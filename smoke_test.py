import os, json, inspect
from dotenv import load_dotenv
import api_tools_rest_generated as t

load_dotenv()

def ok(label, r):
    print(f"\n[{label}] {json.dumps(r, indent=2)}")
    assert r.get("ok"), r
    return r

ok("auth", t.portal_authenticate(t.AuthParams()))

# 1) try expected path-based name
mods = None
if hasattr(t, "get_api_v1_models") and hasattr(t, "GetApiV1ModelsParams"):
    mods = ok("list_models (path-based)",
              t.get_api_v1_models(t.GetApiV1ModelsParams())
             )["response"]

# 2) else try introspection for any '*models*' tool
if mods is None:
    for name, obj in vars(t).items():
        if callable(obj) and "models" in name.lower() and not name.endswith("Params"):
            # find matching Params class (assumes Name + 'Params')
            params_name = name[0].upper() + name[1:] + "Params"
            params_cls = getattr(t, params_name, None)
            if params_cls:
                try:
                    mods = ok(f"list_models ({name})", getattr(t, name)(params_cls()))["response"]
                    break
                except Exception as e:
                    print(f"Attempt {name} failed: {e}")

# 3) else fall back to generic
if mods is None:
    mods = ok("list_models (generic)",
              t.portal_request(t.PortalRequestParams(method="GET", path="/api/v1/models"))
             )["response"]

print("Model count:", len(mods))
