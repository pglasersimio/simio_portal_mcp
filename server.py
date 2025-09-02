import os, time
from typing import Optional
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# --- env ---
load_dotenv()
PORTAL_URL = os.environ.get("SIMIO_PORTAL_URL", "").rstrip("/")
PAT = os.environ.get("PERSONAL_ACCESS_TOKEN", "")
DEFAULT_PROJECT = os.environ.get("PROJECT_NAME")

# --- lazy import pysimio so discovery is fast ---
_api = None
def api():
    global _api
    if _api is None:
        try:
            from pysimio import pySimio
        except Exception as e:
            raise RuntimeError("pysimio import failed. Install deps with `pip install -e .`") from e
        if not PORTAL_URL:
            raise ValueError("SIMIO_PORTAL_URL is not set. Provide it in .env")
        _api = pySimio(PORTAL_URL)
        if PAT:
            _api.authenticate(personalAccessToken=PAT)
    return _api

# --- retry policy ---
retryable = retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(Exception),
)

mcp = FastMCP("SimioPortalTools")

# ------------ Models ------------
class AuthParams(BaseModel):
    personal_access_token: Optional[str] = Field(None, description="Overrides env PAT")

class ListModelsParams(BaseModel): pass
class GetModelIdByProjectParams(BaseModel):
    project_name: Optional[str] = Field(None, description="Overrides PROJECT_NAME")
class ListExperimentsParams(BaseModel):
    model_id: str
class GetDefaultExperimentParams(BaseModel):
    model_id: str
class ListRunsParams(BaseModel):
    experiment_id: str
class StartOrGetRunParams(BaseModel):
    experiment_id: str
    run_name: str
    create_if_missing: bool = True
class StartRunParams(BaseModel):
    experiment_id: str
    run_id: str
class RunStatusParams(BaseModel):
    experiment_id: str
    run_id: str
    include_children: bool = True
class PollUntilCompleteParams(BaseModel):
    experiment_id: str
    run_id: str
    interval_secs: float = 5
    timeout_secs: float = 3600

# ------------ Tools ------------
@mcp.tool()
@retryable
def portal_authenticate(params: AuthParams) -> dict:
    a = api()
    pat = params.personal_access_token or PAT
    if not pat:
        raise ValueError("No PAT provided")
    a.authenticate(personalAccessToken=pat)
    return {"ok": True}

@mcp.tool()
@retryable
def list_models(params: ListModelsParams) -> list:
    a = api()
    return a.getModels()

@mcp.tool()
@retryable
def get_model_id_by_project(params: GetModelIdByProjectParams) -> dict:
    project = (params.project_name or DEFAULT_PROJECT or "").strip()
    if not project:
        raise ValueError("Provide project_name or set PROJECT_NAME")
    models = api().getModels()
    for m in models:
        if m.get("projectName", "").lower() == project.lower():
            return {"model_id": m["id"], "model_name": m.get("name")}
    raise ValueError(f"Project '{project}' not found")

@mcp.tool()
@retryable
def list_experiments(params: ListExperimentsParams) -> list:
    return api().getExperiments(modelId=params.model_id)

@mcp.tool()
@retryable
def get_default_experiment_id(params: GetDefaultExperimentParams) -> dict:
    exps = api().getExperiments(modelId=params.model_id)
    for e in exps:
        if e.get("name") == "__Default":
            return {"experiment_id": e["id"]}
    raise ValueError("Default experiment '__Default' not found")

@mcp.tool()
@retryable
def list_runs(params: ListRunsParams) -> list:
    return api().getRuns(experimentId=params.experiment_id)

@mcp.tool()
@retryable
def start_or_get_run(params: StartOrGetRunParams) -> dict:
    runs = api().getRuns(experimentId=params.experiment_id)
    for r in runs:
        if r.get("name") == params.run_name:
            return {"run_id": r["id"], "created": False}
    if not params.create_if_missing:
        raise ValueError("Run not found")
    r = api().createRun(experimentId=params.experiment_id, name=params.run_name)
    return {"run_id": r["id"], "created": True}

@mcp.tool()
@retryable
def start_run(params: StartRunParams) -> dict:
    api().startRun(experimentId=params.experiment_id, runId=params.run_id)
    return {"ok": True}

@mcp.tool()
@retryable
def get_run_status(params: RunStatusParams) -> dict:
    detail = api().getRun(experimentId=params.experiment_id, runId=params.run_id)
    out = {
        "state": detail.get("state"),
        "percentComplete": detail.get("percentComplete"),
        "started": detail.get("startDateTimeUtc"),
        "finished": detail.get("endDateTimeUtc"),
    }
    if params.include_children:
        out["children"] = api().getRuns(experimentId=params.experiment_id, parentRunId=params.run_id)
    return out

@mcp.tool()
def poll_until_complete(params: PollUntilCompleteParams) -> dict:
    start = time.time()
    while True:
        s = get_run_status(RunStatusParams(experiment_id=params.experiment_id, run_id=params.run_id))
        state = s["state"]
        if state in ("COMPLETED", "FAILED", "ERROR", "CANCELED"):
            return {"final_state": state, "elapsed_secs": round(time.time() - start, 2), **s}
        if time.time() - start > params.timeout_secs:
            return {"final_state": "TIMEOUT", "elapsed_secs": round(time.time() - start, 2), **s}
        time.sleep(params.interval_secs)

if __name__ == "__main__":
    mcp.run()
