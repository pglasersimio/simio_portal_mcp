# workflow_tools.py
"""
High-level MCP tools ("workflows") that orchestrate multiple pysimio calls directly.
These do NOT depend on the atomic tools; they call pysimio via portal_adapter.call
and helpers.api.

Workflow included:
  - create_or_replace_plan_run
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from mcp_app import mcp
from helpers import wrap_errors, retryable, MCPValidationError, MCPApiError, api
from portal_adapter import call

# ------------------ Pydantic input models ------------------

class CreateOrReplacePlanRunParams(BaseModel):
    # Resolution
    project_name: str = Field(..., min_length=1, description="Simio projectName to resolve model")
    experiment_name: str = Field("__Default", min_length=1, description="Experiment name to use")

    # New run
    plan_name: str = Field(..., min_length=1, description="Run name (the plan name)")

    # Optional configuration
    controls: Optional[Dict[str, Any]] = Field(None, description="ControlName -> value map")
    start_time: Optional[str] = Field(
        None,
        description="ISO8601 start (e.g. '2025-12-13T03:14:00Z'); set use_specific_start automatically"
    )
    end_time: Optional[str] = Field(
        None,
        description="ISO8601 end (e.g. '2025-12-20T03:14:00Z'); set use_specific_end automatically"
    )

    # Behavior
    delete_existing: bool = Field(True, description="Delete existing run with same name before create")
    start_mode: str = Field("standard", description="'standard' uses startRun; 'from_existing' uses startRunFromExisting")
    run_plan: bool = Field(True, description="Only for start_mode='from_existing'")
    run_replications: bool = Field(False, description="Only for start_mode='from_existing'")

    # Polling
    poll: bool = Field(True, description="Poll until terminal state")
    interval_secs: float = Field(10.0, ge=0.5, le=60)
    timeout_secs: float = Field(3600.0, ge=5, le=24*3600)

    # Dry-run
    dry_run: bool = Field(False, description="If true, perform discovery and return planned actions without mutating")

    @field_validator("start_mode")
    @classmethod
    def _check_mode(cls, v):
        v2 = v.strip().lower()
        if v2 not in {"standard", "from_existing"}:
            raise MCPValidationError("start_mode must be 'standard' or 'from_existing'")
        return v2

# ------------------ Helpers ------------------

def _iso(dt: Optional[str]) -> Optional[str]:
    if not dt:
        return None
    s = dt.strip()
    if not s:
        return None
    # Allow naive ISO (add Z) or pass-through if already Z
    if s.endswith("Z"):
        return s
    try:
        # Validate it parses
        datetime.fromisoformat(s)
        return s + "Z"
    except Exception:
        # If it already includes offset like +00:00 keep it
        try:
            datetime.fromisoformat(s.replace("Z", "+00:00"))
            return s
        except Exception:
            raise MCPValidationError(f"Invalid ISO datetime: {dt}")

def _terminal(state: Optional[str]) -> bool:
    return (state or "").upper() in {"COMPLETED", "FAILED", "ERROR", "CANCELED"}

# ------------------ Workflow tool ------------------

@mcp.tool()
@wrap_errors
@retryable
def create_or_replace_plan_run(params: CreateOrReplacePlanRunParams) -> dict:
    """
    Resolve model by project -> experiment -> (optional) delete same-name run -> create run -> set controls/time -> start -> (optional) poll.
    Returns IDs and (if polled) a final status snapshot.
    Assumes you've already authenticated via portal_authenticate.
    """
    # 1) Resolve model by project
    models = call("getModels") or []
    model = next((m for m in models if (m.get("projectName") or "").lower() == params.project_name.lower()), None)
    if not model:
        raise MCPApiError(f"Project '{params.project_name}' not found in getModels()")
    model_id = model["id"]

    # 2) Resolve experiment by name
    experiments = call("getExperiments", model_id=model_id) or []
    exp = next((e for e in experiments if (e.get("name") or "").strip().lower() == params.experiment_name.strip().lower()), None)
    if not exp:
        names = [e.get("name") for e in experiments]
        raise MCPApiError(f"Experiment '{params.experiment_name}' not found for model {model_id}. Available: {names}")
    experiment_id = exp["id"]

    # Prepare result shell
    result = {
        "project_name": params.project_name,
        "model_id": model_id,
        "experiment_name": params.experiment_name,
        "experiment_id": experiment_id,
        "plan_name": params.plan_name,
        "actions": [],
    }

    # 3) Find existing run by name (exact, case-insensitive)
    runs = call("getRuns", experiment_id=experiment_id) or []
    existing = next((r for r in runs if (r.get("name") or "").strip().lower() == params.plan_name.strip().lower()), None)

    if existing and params.delete_existing:
        result["actions"].append({"deleteRun": existing["id"]})
        if not params.dry_run:
            call("deleteRun", run_id=existing["id"])

    # 4) Create new run
    result["actions"].append({"createRun": {"experiment_id": experiment_id, "name": params.plan_name}})
    if params.dry_run:
        run_id = "DRY_RUN_PLACEHOLDER"
    else:
        created = call("createRun", experiment_id=experiment_id, name=params.plan_name)
        run_id = created["id"]
    result["run_id"] = run_id

    # 5) Set control values
    if params.controls:
        for k, v in params.controls.items():
            result["actions"].append({"setControlValues": {"run_id": run_id, "scenario": params.plan_name, "name": k, "value": str(v)}})
            if not params.dry_run:
                call(
                    "setControlValues",
                    run_id=run_id,
                    scenario_name=params.plan_name,
                    control_name=k,
                    control_value=str(v),
                )

    # 6) Set run time options
    st = _iso(params.start_time)
    et = _iso(params.end_time)
    if st or et:
        result["actions"].append({"setRunTimeOptions": {"run_id": run_id, "start": st, "end": et}})
        if not params.dry_run:
            # Build TimeOptions and pass via adapter (supports snake/camel)
            from pysimio.classes import TimeOptions
            opts = TimeOptions(
                runId=run_id,
                isSpecificStartTime=bool(st),
                specificStartingTime=st,
                isSpecificEndTime=bool(et),
                specificEndingTime=et,
            )
            # Some pysimio builds take positional TimeOptions, others expect kw `timeOptions`
            try:
                call("setRunTimeOptions", time_options=opts)
            except MCPApiError:
                # Fallback: try direct client if adapter mapping isn't enough
                api().setRunTimeOptions(opts)

    # 7) Start the run
    if params.start_mode == "standard":
        result["actions"].append({"startRun": {"experiment_id": experiment_id, "run_id": run_id}})
        if not params.dry_run:
            call("startRun", experiment_id=experiment_id, run_id=run_id)
    else:  # from_existing
        result["actions"].append({"startRunFromExisting": {"run_id": run_id, "runPlan": params.run_plan, "runReplications": params.run_replications}})
        if not params.dry_run:
            call(
                "startRunFromExisting",
                existing_experiment_run_id=run_id,
                run_plan=params.run_plan,
                run_replications=params.run_replications,
            )

    # 8) Optional poll to completion
    if params.poll and not params.dry_run:
        import time
        start_ts = time.time()
        last = {}
        while True:
            detail = call("getRun", experiment_id=experiment_id, run_id=run_id) or {}
            last = {
                "state": detail.get("state"),
                "percentComplete": detail.get("percentComplete"),
                "started": detail.get("startDateTimeUtc"),
                "finished": detail.get("endDateTimeUtc"),
            }
            if _terminal(last["state"]):
                result["final"] = last
                result["elapsed_secs"] = round(time.time() - start_ts, 2)
                break
            if time.time() - start_ts > params.timeout_secs:
                result["final"] = {"state": "TIMEOUT", **last}
                result["elapsed_secs"] = round(time.time() - start_ts, 2)
                break
            time.sleep(params.interval_secs)

    return {"ok": True, **result}
