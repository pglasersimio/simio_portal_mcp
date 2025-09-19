# portal_adapter.py
from helpers import api, MCPApiError

_SNAKE_TO_CAMEL = {
    "model_id": "modelId",
    "experiment_id": "experimentId",
    "parent_run_id": "parentRunId",
    "run_id": "runId",
    "existing_experiment_run_id": "existingExperimentRunId",
    "run_plan": "runPlan",
    "run_replications": "runReplications",
    "scenario_name": "scenarioName",
    "control_name": "controlName",
    "control_value": "controlValue",
    "time_options": "timeOptions",
}

def _alt_kwargs(kwargs: dict) -> dict:
    out = dict(kwargs)
    for k, v in list(kwargs.items()):
        ck = _SNAKE_TO_CAMEL.get(k)
        if ck:
            out[ck] = v
    return out

def call(method: str, **kwargs):
    """Call a pysimio method. Try snake_case first, then camelCase kwargs."""
    a = api()
    fn = getattr(a, method)
    try:
        return fn(**kwargs)
    except TypeError as e1:
        try:
            return fn(**_alt_kwargs(kwargs))
        except TypeError as e2:
            raise MCPApiError(f"{method} signature mismatch: {e1} || {e2}")
