"""
AUTO-GENERATED MCP tools from swagger.json at 2025-09-05T19:43:19.771981Z.
Each endpoint is exposed as an MCP tool with a Pydantic params model.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from mcp_app import mcp
from rest_client_generated import SimioClientGenerated, SimioApiError

retryable = retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(Exception),
)

def ok(payload: Any) -> Dict[str, Any]:
    return {"ok": True, **(payload if isinstance(payload, dict) else {"data": payload})}

def err(exc: Exception) -> Dict[str, Any]:
    return {"ok": False, "error": {"type": exc.__class__.__name__, "message": str(exc)}}

class RestAuthParams(BaseModel):
    personal_access_token: Optional[str] = Field(None, description="Overrides env PERSONAL_ACCESS_TOKEN")

# Backwards-compat alias for callers expecting AuthParams
AuthParams = RestAuthParams

@mcp.tool()
@retryable
def portal_authenticate(params: RestAuthParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        token = c.authenticate(params.personal_access_token)
        return ok({"message": "Authenticated", "token_prefix": token[:12] + "..."})
    except Exception as e:
        return err(e)

class RequesttokenPostrestapitokenrequestParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def requesttoken_postrestapitokenrequest(params: RequesttokenPostrestapitokenrequestParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.requesttoken_postrestapitokenrequest(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ExperimentsGetexperimentsParams(BaseModel):
    query: Optional[dict] = None

@mcp.tool()
@retryable
def experiments_getexperiments(params: ExperimentsGetexperimentsParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.experiments_getexperiments(query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ExperimentsGetexperimentbyidParams(BaseModel):
    experiment_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def experiments_getexperimentbyid(params: ExperimentsGetexperimentbyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.experiments_getexperimentbyid(experiment_id=params.experiment_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class HeartbeatGetParams(BaseModel):
    query: Optional[dict] = None

@mcp.tool()
@retryable
def heartbeat_get(params: HeartbeatGetParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.heartbeat_get(query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ModelsGetmodelsParams(BaseModel):
    query: Optional[dict] = None

@mcp.tool()
@retryable
def models_getmodels(params: ModelsGetmodelsParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.models_getmodels(query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ModelsGetmodelbyidParams(BaseModel):
    model_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def models_getmodelbyid(params: ModelsGetmodelbyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.models_getmodelbyid(model_id=params.model_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ModelsDeletemodelParams(BaseModel):
    model_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def models_deletemodel(params: ModelsDeletemodelParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.models_deletemodel(model_id=params.model_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ModelsGetmodeltableschemaParams(BaseModel):
    model_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def models_getmodeltableschema(params: ModelsGetmodeltableschemaParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.models_getmodeltableschema(model_id=params.model_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ProjectsUploadParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict] = None

@mcp.tool()
@retryable
def projects_upload(params: ProjectsUploadParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.projects_upload(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ProjectsDeleteprojectParams(BaseModel):
    project_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def projects_deleteproject(params: ProjectsDeleteprojectParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.projects_deleteproject(project_id=params.project_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ProjectsGetprojectbyidParams(BaseModel):
    project_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def projects_getprojectbyid(params: ProjectsGetprojectbyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.projects_getprojectbyid(project_id=params.project_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ProjectsGetParams(BaseModel):
    query: Optional[dict] = None

@mcp.tool()
@retryable
def projects_get(params: ProjectsGetParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.projects_get(query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class PublishedplansPublishplanParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def publishedplans_publishplan(params: PublishedplansPublishplanParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.publishedplans_publishplan(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class PublishedplansUploadandpublishplanParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict] = None

@mcp.tool()
@retryable
def publishedplans_uploadandpublishplan(params: PublishedplansUploadandpublishplanParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.publishedplans_uploadandpublishplan(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class PublishedrunsPublishexperimentrunParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def publishedruns_publishexperimentrun(params: PublishedrunsPublishexperimentrunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.publishedruns_publishexperimentrun(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class PublishedrunsDeletepublishedrunParams(BaseModel):
    published_name: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def publishedruns_deletepublishedrun(params: PublishedrunsDeletepublishedrunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.publishedruns_deletepublishedrun(published_name=params.published_name, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsGetParams(BaseModel):
    query: Optional[dict] = None

@mcp.tool()
@retryable
def runs_get(params: RunsGetParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_get(query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsGetrunbyidParams(BaseModel):
    run_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def runs_getrunbyid(params: RunsGetrunbyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_getrunbyid(run_id=params.run_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsDeleterunParams(BaseModel):
    run_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def runs_deleterun(params: RunsDeleterunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_deleterun(run_id=params.run_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsCancelrunParams(BaseModel):
    run_id: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_cancelrun(params: RunsCancelrunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_cancelrun(run_id=params.run_id, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsSetscenariostartendtypeParams(BaseModel):
    run_id: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_setscenariostartendtype(params: RunsSetscenariostartendtypeParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_setscenariostartendtype(run_id=params.run_id, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsCancelrunwithadditionalrunidParams(BaseModel):
    run_id: str
    additional_run_id: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_cancelrunwithadditionalrunid(params: RunsCancelrunwithadditionalrunidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_cancelrunwithadditionalrunid(run_id=params.run_id, additional_run_id=params.additional_run_id, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsCreateexperimentrunParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_createexperimentrun(params: RunsCreateexperimentrunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_createexperimentrun(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsCreateexperimentrunfromexistingParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_createexperimentrunfromexisting(params: RunsCreateexperimentrunfromexistingParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_createexperimentrunfromexisting(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsStartexistingplanrunParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_startexistingplanrun(params: RunsStartexistingplanrunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_startexistingplanrun(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class RunsStartexperimentrunParams(BaseModel):
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def runs_startexperimentrun(params: RunsStartexperimentrunParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.runs_startexperimentrun(query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosRenameexperimentrunscenarioParams(BaseModel):
    run_id: str
    scenario_name: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def scenarios_renameexperimentrunscenario(params: ScenariosRenameexperimentrunscenarioParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_renameexperimentrunscenario(run_id=params.run_id, scenario_name=params.scenario_name, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosSetexperimentrunscenariocontrolvalueParams(BaseModel):
    run_id: str
    scenario_name: str
    control_name: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def scenarios_setexperimentrunscenariocontrolvalue(params: ScenariosSetexperimentrunscenariocontrolvalueParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_setexperimentrunscenariocontrolvalue(run_id=params.run_id, scenario_name=params.scenario_name, control_name=params.control_name, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosSetexperimentrunscenariodataconnectorconfigurationsParams(BaseModel):
    run_id: str
    scenario_name: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def scenarios_setexperimentrunscenariodataconnectorconfigurations(params: ScenariosSetexperimentrunscenariodataconnectorconfigurationsParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_setexperimentrunscenariodataconnectorconfigurations(run_id=params.run_id, scenario_name=params.scenario_name, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosExporttablesandlogsParams(BaseModel):
    run_id: str
    scenario_name: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_exporttablesandlogs(params: ScenariosExporttablesandlogsParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_exporttablesandlogs(run_id=params.run_id, scenario_name=params.scenario_name, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosGetexportbyidParams(BaseModel):
    run_id: str
    export_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_getexportbyid(params: ScenariosGetexportbyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_getexportbyid(run_id=params.run_id, export_id=params.export_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosImportexperimentrunscenariotabledataParams(BaseModel):
    run_id: str
    scenario_name: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_importexperimentrunscenariotabledata(params: ScenariosImportexperimentrunscenariotabledataParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_importexperimentrunscenariotabledata(run_id=params.run_id, scenario_name=params.scenario_name, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosGetimportbyidParams(BaseModel):
    run_id: str
    import_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_getimportbyid(params: ScenariosGetimportbyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_getimportbyid(run_id=params.run_id, import_id=params.import_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosSetexperimentrunscenariotablevalueParams(BaseModel):
    run_id: str
    scenario_name: str
    table_name: str
    query: Optional[dict] = None
    body: Optional[dict]

@mcp.tool()
@retryable
def scenarios_setexperimentrunscenariotablevalue(params: ScenariosSetexperimentrunscenariotablevalueParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_setexperimentrunscenariotablevalue(run_id=params.run_id, scenario_name=params.scenario_name, table_name=params.table_name, query=params.query, body=params.body)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosInsertexperimentrunscenariotablerowParams(BaseModel):
    run_id: str
    scenario_name: str
    table_name: str
    row_index: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_insertexperimentrunscenariotablerow(params: ScenariosInsertexperimentrunscenariotablerowParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_insertexperimentrunscenariotablerow(run_id=params.run_id, scenario_name=params.scenario_name, table_name=params.table_name, row_index=params.row_index, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosRemoveexperimentrunscenariotablerowParams(BaseModel):
    run_id: str
    scenario_name: str
    table_name: str
    row_index: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_removeexperimentrunscenariotablerow(params: ScenariosRemoveexperimentrunscenariotablerowParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_removeexperimentrunscenariotablerow(run_id=params.run_id, scenario_name=params.scenario_name, table_name=params.table_name, row_index=params.row_index, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosGetscenarioresponsedatabyidParams(BaseModel):
    run_id: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_getscenarioresponsedatabyid(params: ScenariosGetscenarioresponsedatabyidParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_getscenarioresponsedatabyid(run_id=params.run_id, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)

class ScenariosGetscenariotablerowdataParams(BaseModel):
    run_id: str
    scenario_name: str
    table_name: str
    query: Optional[dict] = None

@mcp.tool()
@retryable
def scenarios_getscenariotablerowdata(params: ScenariosGetscenariotablerowdataParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token:
            c.authenticate()
        data = c.scenarios_getscenariotablerowdata(run_id=params.run_id, scenario_name=params.scenario_name, table_name=params.table_name, query=params.query)
        return ok({'response': data})
    except Exception as e:
        return err(e)


class PortalRequestParams(BaseModel):
    method: str = Field(..., pattern="^(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD|TRACE)$")
    path: str = Field(..., min_length=1)
    query: Optional[dict] = None
    body: Optional[dict] = None

@mcp.tool()
@retryable
def portal_request(params: PortalRequestParams) -> dict:
    try:
        c = SimioClientGenerated.from_env()
        if not c.token: c.authenticate()
        data = c.request(params.method, params.path, params=params.query, json=params.body)
        return ok({"response": data})
    except Exception as e:
        return err(e)

if __name__ == "__main__":
    mcp.run()
