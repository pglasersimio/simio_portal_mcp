# mcp-simio (pysimio-backed MCP server)

Minimal MCP server that exposes Simio Portal operations (`pysimio`) as tools you can call from ChatGPT or any MCP client.

## What you get
- `portal_authenticate` — login with PAT
- `list_models` — enumerate models
- `get_model_id_by_project` — resolve model by project name
- `list_experiments` — list experiments for a model
- `get_default_experiment_id` — find `__Default` experiment
- `list_runs` — list runs under an experiment
- `start_or_get_run` — idempotently get/create a run by name
- `start_run` — start execution
- `get_run_status` — check state/percent/child runs
- `poll_until_complete` — loop until terminal state

## Prereqs
- Python 3.10+
- A Simio Portal instance and a **Personal Access Token (PAT)**
- Network access to the Portal URL

## Setup

1) Clone or unzip this repo.
2) Create `.env` from `.env.example` and fill the values:
   ```env
   SIMIO_PORTAL_URL=https://your-portal-host
   PERSONAL_ACCESS_TOKEN=...
   PROJECT_NAME=OptionalProjectName
   ```
3) Install dependencies (choose one):
   ```bash
   # virtualenv (recommended)
   python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
   pip install -e .
   ```

## Run the MCP server
```bash
python server.py
```

The server speaks MCP over stdio (suitable for desktop clients and bridges).

## Use from an MCP client
- **ChatGPT (Plus/Business/Enterprise desktop or web)**: add a *Custom connector* targeting this local server (stdio/bridge). ChatGPT will discover the tools; then you can invoke them in chat (e.g., “list models”).
- **Other MCP clients**: point them to the same server; tools are self-described.

> Note: If your `pysimio` version uses different method names or return shapes, adjust the few calls inside `server.py` (they’re localized and easy to swap).

## Typical flow
1. Authenticate (optional if PAT is in `.env`):
   ```json
   { "tool": "portal_authenticate", "arguments": { "personal_access_token": "..." } }
   ```
2. Resolve model → experiment:
   - `list_models`
   - `get_model_id_by_project`
   - `list_experiments`
   - `get_default_experiment_id`
3. Create/Start a run and wait:
   - `start_or_get_run` (give it a name)
   - `start_run`
   - `poll_until_complete`

## Troubleshooting
- **ImportError: pysimio** — run `pip install -e .`
- **401/403** — check PAT scope/expiry; re-run `portal_authenticate`
- **URL errors** — verify `SIMIO_PORTAL_URL` (no trailing paths, just the host)
- **Long runs** — increase `timeout_secs` on `poll_until_complete`

## Security
- Keep secrets in `.env`. Do not commit it.
- Least-privilege PATs recommended.
