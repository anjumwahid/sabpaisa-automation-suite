"""
Settings Manager — Reads settings.json + supports ENV variable overrides.
In Docker/CI, set ENV vars to override: ENV, HEADLESS, SLOW_MO, BASE_URL
"""

import json, os

_path = os.path.join(os.path.dirname(__file__), "settings.json")
with open(_path, "r") as f:
    _cfg = json.load(f)

# ENV variable overrides (for Docker / CI / Bitbucket / GitHub Actions)
BASE_URL        = os.getenv("BASE_URL", _cfg["base_url"])
ENVIRONMENT     = os.getenv("ENV", _cfg["environment"])
BROWSER         = os.getenv("BROWSER", _cfg["browser"])
HEADLESS        = os.getenv("HEADLESS", str(_cfg["headless"])).lower() == "true"
SLOW_MO         = int(os.getenv("SLOW_MO", str(_cfg["slow_mo"])))
VIEWPORT        = _cfg["viewport"]
DEFAULT_TIMEOUT = int(os.getenv("TIMEOUT", str(_cfg["default_timeout"])))

# For parallel batch runner
MERCHANT_ID_OVERRIDE = os.getenv("MERCHANT_ID_OVERRIDE", None)
