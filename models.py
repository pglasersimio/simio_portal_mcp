# models.py
from pydantic import BaseModel, Field, model_validator
from typing import Optional
import os
from helpers import MCPValidationError

DEFAULT_PROJECT = os.environ.get("PROJECT_NAME") or None
ENV_PAT = os.environ.get("PERSONAL_ACCESS_TOKEN") or None

class AuthParams(BaseModel):
    personal_access_token: Optional[str] = Field(None, description="Overrides env PERSONAL_ACCESS_TOKEN")
    @model_validator(mode="after")
    def _ensure_token(cls, v: "AuthParams"):
        if not (v.personal_access_token or ENV_PAT):
            raise MCPValidationError("No PAT provided. Pass personal_access_token or set PERSONAL_ACCESS_TOKEN.")
        return v

class GetModelIdByProjectParams(BaseModel):
    project_name: Optional[str] = Field(None, description="Project name; falls back to env PROJECT_NAME")
    @model_validator(mode="after")
    def _default(cls, v: "GetModelIdByProjectParams"):
        proj = (v.project_name or DEFAULT_PROJECT or "").strip() or None
        v.project_name = proj
        return v

class ListModelsParams(BaseModel):
    pass

class ListExperimentsParams(BaseModel):
    model_id: str = Field(..., min_length=1)

class GetExperimentIdByNameParams(BaseModel):
    model_id: str = Field(..., min_length=1)
    experiment_name: str = Field(..., min_length=1)
