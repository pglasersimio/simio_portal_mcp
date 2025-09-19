# tools.py
from mcp_app import mcp
from helpers import api, wrap_errors, retryable, MCPValidationError
import models

# Re-export commonly used models so callers can do: `import tools as m; m.AuthParams(...)`
from models import AuthParams

# ---------- Utility: describe pysimio surface (for LLM planning) ----------
# tools.py (replace describe_pysimio with this)
@mcp.tool()
@wrap_errors
def describe_pysimio(_: dict) -> dict:
    """
    Introspect the pySimio client and return a compact map of
    { method_name: { signature, doc } } for key methods.
    """
    import inspect
    try:
        a = __import__("pysimio", fromlist=["pySimio"])
        client = a.pySimio("about:blank")  # construct without network/auth
    except Exception as e:
        return {"ok": False, "error": {"type": "ImportError", "message": str(e)}}

    methods = [
        "status", "reauthenticate", "authenticate",
        "getModels", "getModel", "getModelTable",
        "getExperiments", "getRuns", "getRun",
        "createRun", "deleteRun",
        "setControlValues", "setRunTimeOptions",
        "startRun", "startRunFromExisting",
    ]

    out = {}
    for name in methods:
        fn = getattr(client, name, None)
        if fn is None:
            continue
        # Try to get signature; fall back gracefully if it's a C-accelerated or wrapped callable
        try:
            sig = str(inspect.signature(fn))
        except Exception:
            # Fallback: try the unbound function on the class
            try:
                sig = str(inspect.signature(getattr(type(client), name)))
            except Exception:
                sig = "()"
        # Doc: first line only
        doc = (getattr(fn, "__doc__", "") or "").strip().splitlines()
        doc1 = (doc[0] if doc else "").strip()
        out[name] = {"signature": sig, "doc": doc1}

    return {"methods": out}

# ---------- Auth ----------
@mcp.tool()
@wrap_errors
@retryable
def portal_authenticate_pysimio(params: models.AuthParams) -> dict:
    """
    Authenticate with PAT (param overrides env).
    """
    pat = params.personal_access_token or models.ENV_PAT
    if not pat:
        raise MCPValidationError(
            "No PAT provided. Pass personal_access_token or set PERSONAL_ACCESS_TOKEN."
        )
    api().authenticate(personalAccessToken=pat)
    return {"message": "Authenticated."}


# ---------- Thin REST-backed tools expected by clients (validation-friendly) ----------
from rest_client_generated import SimioClientGenerated
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ListModelsParams(BaseModel):
    pass

@mcp.tool()
@wrap_errors
@retryable
def list_models(params: ListModelsParams) -> dict:
    """Return list of models visible to this PAT."""
    c = SimioClientGenerated.from_env()
    models_list = c.models_getmodels()
    return {"response": models_list}

class GetModelIdByProjectParams(BaseModel):
    project_name: Optional[str] = Field(None, description="If omitted uses PROJECT_NAME from .env")

@mcp.tool()
@wrap_errors
@retryable
def get_model_id_by_project(params: GetModelIdByProjectParams) -> dict:
    """Find model ID by project name (case-insensitive exact match)."""
    c = SimioClientGenerated.from_env()
    name = params.project_name or models.ENV_PROJECT_NAME
    if not name:
        raise MCPValidationError("project_name is required (or set PROJECT_NAME in .env).")
    all_models = c.models_getmodels()
    matches = [m for m in all_models if str(m.get('projectName','')).lower() == name.lower()]
    if not matches:
        raise MCPValidationError(f"No model found with projectName='{name}'.")
    return {"response": matches[0].get('id')}
