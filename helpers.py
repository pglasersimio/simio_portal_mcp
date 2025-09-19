# helpers.py
import logging
import os
import threading
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

# --- env & logging ---
load_dotenv()
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("SimioPortalMCP")

# --- exceptions ---
class MCPConfigError(RuntimeError): ...
class MCPAuthenticationError(RuntimeError): ...
class MCPValidationError(ValueError): ...
class MCPApiError(RuntimeError): ...

# --- retry policy ---
retryable = retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type(Exception),
)

# --- error wrapper for MCP tools ---
def wrap_errors(fn):
    def _w(*args, **kwargs):
        try:
            res = fn(*args, **kwargs)
            if isinstance(res, dict) and "ok" in res:
                return res
            return {"ok": True, **(res if isinstance(res, dict) else {"data": res})}
        except (MCPConfigError, MCPAuthenticationError, MCPValidationError, MCPApiError) as e:
            log.exception("Handled error in %s", fn.__name__)
            return {"ok": False, "error": {"type": e.__class__.__name__, "message": str(e)}}
        except Exception as e:
            log.exception("Unhandled error in %s", fn.__name__)
            return {"ok": False, "error": {"type": "MCPApiError", "message": str(e)}}
    _w.__name__ = fn.__name__
    _w.__doc__ = fn.__doc__
    return _w

# --- pysimio client (lazy) ---
_api = None
_api_lock = threading.Lock()

def api():
    """Create/load a pysimio client using SIMIO_PORTAL_URL."""
    from pysimio import pySimio  # import here so discovery is fast
    portal_url = (os.environ.get("SIMIO_PORTAL_URL") or "").rstrip("/")
    if not portal_url:
        raise MCPConfigError("SIMIO_PORTAL_URL is not set. Put it in your .env")
    global _api
    with _api_lock:
        if _api is None:
            _api = pySimio(portal_url)
    return _api
