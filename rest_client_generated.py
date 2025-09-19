"""
AUTO-GENERATED client from swagger.json at 2025-09-05T19:43:19.771981Z.
This file provides SimioClientGenerated with one method per endpoint.
Lightweight: uses requests and a single request() utility.
"""


import os
import time
import requests
from typing import Any, Dict, Optional
from dataclasses import dataclass
from requests import Response

class SimioApiError(RuntimeError): ...
def _join(base: str, path: str) -> str:
    return f"{base.rstrip('/')}{path}"

@dataclass
class SimioClientGenerated:
    base_url: str
    token: Optional[str] = None
    session: requests.Session = requests.Session()

    @classmethod
    def from_env(cls) -> "SimioClientGenerated":
        base = os.getenv("SIMIO_PORTAL_URL", "").strip()
        if not base:
            raise SimioApiError("SIMIO_PORTAL_URL must be set")
        return cls(base_url=base)

    def _headers(self) -> Dict[str,str]:
        h = {"Accept":"application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _handle(self, r: Response):
        if r.status_code >= 400:
            try: data = r.json()
            except Exception: data = r.text
            raise SimioApiError(f"{r.status_code} {r.request.method} {r.url}: {data}")
        if r.status_code == 204:
            return None
        if "application/json" in (r.headers.get("Content-Type","")):
            return r.json()
        try: return r.json()
        except Exception: return r.text

    def request(self, method: str, path: str, *, params=None, json=None, timeout=60):
        url = _join(self.base_url, path)
        r = self.session.request(method.upper(), url, headers=self._headers(), params=params, json=json, timeout=timeout)
        if r.status_code == 429:
            ra = r.headers.get("Retry-After")
            if ra:
                time.sleep(float(ra))
            # fall through to error handling
        return self._handle(r)

    def authenticate(self, personal_access_token: Optional[str] = None) -> str:
        pat = personal_access_token or os.getenv("PERSONAL_ACCESS_TOKEN")
        if not pat:
            raise SimioApiError("No PAT provided")
        data = self.request("POST", "/api/auth", json={"personalAccessToken": pat})
        token = (data or {}).get("token")
        if not token:
            raise SimioApiError("Auth succeeded but no token returned")
        self.token = token
        return token

    def requesttoken_postrestapitokenrequest( self, query: dict | None = None, body: dict | None = None ):
        """"""
        path = f"/api/auth"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def experiments_getexperiments( self, query: dict | None = None ):
        """Retrieves a collection of experiments."""
        path = f"/api/v1/experiments"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def experiments_getexperimentbyid( self, experiment_id: str, query: dict | None = None ):
        """Retrieves an experiment using its corresponding ID."""
        path = f"/api/v1/experiments/{experiment_id}"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def heartbeat_get( self, query: dict | None = None ):
        """Verifies server status."""
        path = f"/api/v1/heartbeat"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def models_getmodels( self, query: dict | None = None ):
        """Retrieves a collection of models."""
        path = f"/api/v1/models"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def models_getmodelbyid( self, model_id: str, query: dict | None = None ):
        """Retrieves a model using its corresponding ID."""
        path = f"/api/v1/models/{model_id}"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def models_deletemodel( self, model_id: str, query: dict | None = None ):
        """Deletes the model matching the specified model ID."""
        path = f"/api/v1/models/{model_id}"
        params = query or None
        return self.request('DELETE', path, params=params, json=None)

    def models_getmodeltableschema( self, model_id: str, query: dict | None = None ):
        """Retrieves a collection of model table schemas."""
        path = f"/api/v1/models/{model_id}/table-schemas"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def projects_upload( self, query: dict | None = None, body: dict | None = None ):
        """Uploads and saves the project to the specified named project."""
        path = f"/api/v1/projects/upload"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def projects_deleteproject( self, project_id: str, query: dict | None = None ):
        """Deletes the project matching the specified project ID."""
        path = f"/api/v1/projects/{project_id}"
        params = query or None
        return self.request('DELETE', path, params=params, json=None)

    def projects_getprojectbyid( self, project_id: str, query: dict | None = None ):
        """Retrieves a project using its corresponding ID."""
        path = f"/api/v1/projects/{project_id}"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def projects_get( self, query: dict | None = None ):
        """Retrieves a collection of projects."""
        path = f"/api/v1/projects"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def publishedplans_publishplan( self, query: dict | None = None, body: dict | None = None ):
        """Publishes the plan results of a single scenario of an experiment run to a named published plan result."""
        path = f"/api/v1/published-plans/publish-plan"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def publishedplans_uploadandpublishplan( self, query: dict | None = None, body: dict | None = None ):
        """Uploads and publishes the plan results of a single scenario of an experiment run to a named published plan result."""
        path = f"/api/v1/published-plans/upload-and-publish-plan"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def publishedruns_publishexperimentrun( self, query: dict | None = None, body: dict | None = None ):
        """Publishes an existing experiment run as a named published experiment result."""
        path = f"/api/v1/published-runs"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def publishedruns_deletepublishedrun( self, published_name: str, query: dict | None = None ):
        """Deletes a published experiment run based on the specified publish name."""
        path = f"/api/v1/published-runs/{published_name}"
        params = query or None
        return self.request('DELETE', path, params=params, json=None)

    def runs_get( self, query: dict | None = None ):
        """Retrieves a collection of 'top level' experiment runs, those created as ExperimentRuns,
or those started to run replications for an existing experiment. Note that plan only runs will show up
as child runs in AdditionalRunsStatus."""
        path = f"/api/v1/runs"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def runs_getrunbyid( self, run_id: str, query: dict | None = None ):
        """Retrieves a run using its corresponding ID."""
        path = f"/api/v1/runs/{run_id}"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def runs_deleterun( self, run_id: str, query: dict | None = None ):
        """Deletes the experiment run matching the specified experiment run ID."""
        path = f"/api/v1/runs/{run_id}"
        params = query or None
        return self.request('DELETE', path, params=params, json=None)

    def runs_cancelrun( self, run_id: str, query: dict | None = None, body: dict | None = None ):
        """Cancels a currently running experiment run using the provided experiment run ID."""
        path = f"/api/v1/runs/{run_id}"
        params = query or None
        return self.request('PATCH', path, params=params, json=body)

    def runs_setscenariostartendtype( self, run_id: str, query: dict | None = None, body: dict | None = None ):
        """Sets the start and end time options for an experiment run."""
        path = f"/api/v1/runs/{run_id}/time-options"
        params = query or None
        return self.request('PUT', path, params=params, json=body)

    def runs_cancelrunwithadditionalrunid( self, run_id: str, additional_run_id: str, query: dict | None = None, body: dict | None = None ):
        """Cancels a currently running plan run using the provided parent experiment run ID and additional run ID."""
        path = f"/api/v1/runs/{run_id}/additional-runs/{additional_run_id}"
        params = query or None
        return self.request('PATCH', path, params=params, json=body)

    def runs_createexperimentrun( self, query: dict | None = None, body: dict | None = None ):
        """Creates a new plan run. (PLAN RUNS ONLY)"""
        path = f"/api/v1/runs/create"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def runs_createexperimentrunfromexisting( self, query: dict | None = None, body: dict | None = None ):
        """Creates a new plan run from an existing plan run. (PLAN RUNS ONLY)"""
        path = f"/api/v1/runs/create-from-existing"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def runs_startexistingplanrun( self, query: dict | None = None, body: dict | None = None ):
        """Starts an existing plan run. The ID returned here can be retrieved by making a GET request to /runs and 
passing in the ExperimentId. In the results, the "additionalRunsStatus" will contain the ID returned
from this call. To run Risk Analysis, make sure runReplications is true. (PLAN RUNS ONLY)"""
        path = f"/api/v1/runs/start-existing-plan-run"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def runs_startexperimentrun( self, query: dict | None = None, body: dict | None = None ):
        """Creates and starts an experiment run (NOT FOR PLAN RUNS).
Once the project is uploaded, you can get the experiment id /api/v1/experiments/{model_id}
To update control parameters, you would add them to the "scenarios" section in the json
and run it again.
These following json contains the minimum parameters required to run an experiment.
{
    "ExperimentId": ExperimentId,
    "Name": "ExperimentName",
    "CreateInfo": {
        "Scenarios": [
        {
        "Name": "ScenarioName",
        "ReplicationsRequired": 1
        }
        ]
    }    
}"""
        path = f"/api/v1/runs/start-experiment-run"
        params = query or None
        return self.request('POST', path, params=params, json=body)

    def scenarios_renameexperimentrunscenario( self, run_id: str, scenario_name: str, query: dict | None = None, body: dict | None = None ):
        """Renames the specified scenario of the experiment run."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/name"
        params = query or None
        return self.request('PUT', path, params=params, json=body)

    def scenarios_setexperimentrunscenariocontrolvalue( self, run_id: str, scenario_name: str, control_name: str, query: dict | None = None, body: dict | None = None ):
        """Modifies a control value for the specified scenario of the experiment run."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/control-values/{control_name}"
        params = query or None
        return self.request('PUT', path, params=params, json=body)

    def scenarios_setexperimentrunscenariodataconnectorconfigurations( self, run_id: str, scenario_name: str, query: dict | None = None, body: dict | None = None ):
        """Modifies the active configuration names of data connector configurations for a plan run scenario."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/data-connector-configurations"
        params = query or None
        return self.request('PATCH', path, params=params, json=body)

    def scenarios_exporttablesandlogs( self, run_id: str, scenario_name: str, query: dict | None = None ):
        """Begins an export of table and log data using the export bindings associated with the scenario."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/exports"
        params = query or None
        return self.request('POST', path, params=params, json=None)

    def scenarios_getexportbyid( self, run_id: str, export_id: str, query: dict | None = None ):
        """Retrieves the status of an export using its ID."""
        path = f"/api/v1/runs/{run_id}/scenarios/exports/{export_id}"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def scenarios_importexperimentrunscenariotabledata( self, run_id: str, scenario_name: str, query: dict | None = None ):
        """Begins an import of table data using the import bindings associated with the scenario."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/imports"
        params = query or None
        return self.request('POST', path, params=params, json=None)

    def scenarios_getimportbyid( self, run_id: str, import_id: str, query: dict | None = None ):
        """Retrieves the status of an import using its ID."""
        path = f"/api/v1/runs/{run_id}/scenarios/imports/{import_id}"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def scenarios_setexperimentrunscenariotablevalue( self, run_id: str, scenario_name: str, table_name: str, query: dict | None = None, body: dict | None = None ):
        """Updates a value in an experiment run scenario table."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/table-data/{table_name}/rows"
        params = query or None
        return self.request('PATCH', path, params=params, json=body)

    def scenarios_insertexperimentrunscenariotablerow( self, run_id: str, scenario_name: str, table_name: str, row_index: str, query: dict | None = None ):
        """Inserts a row in an experiment run scenario table at a specified zero-based row index."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/table-data/{table_name}/rows/{row_index}"
        params = query or None
        return self.request('POST', path, params=params, json=None)

    def scenarios_removeexperimentrunscenariotablerow( self, run_id: str, scenario_name: str, table_name: str, row_index: str, query: dict | None = None ):
        """Removes a row in an experiment run scenario table at a specified zero-based row index."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/table-data/{table_name}/rows/{row_index}"
        params = query or None
        return self.request('DELETE', path, params=params, json=None)

    def scenarios_getscenarioresponsedatabyid( self, run_id: str, query: dict | None = None ):
        """Retrieves an experiments run, control values and response data using its corresponding experiment run ID."""
        path = f"/api/v1/runs/{run_id}/scenarios"
        params = query or None
        return self.request('GET', path, params=params, json=None)

    def scenarios_getscenariotablerowdata( self, run_id: str, scenario_name: str, table_name: str, query: dict | None = None ):
        """Retrieves a collection of table row data from an experiment run scenario table."""
        path = f"/api/v1/runs/{run_id}/scenarios/{scenario_name}/table-data/{table_name}"
        params = query or None
        return self.request('GET', path, params=params, json=None)
