# The application run-time configuration (using '.env').
# Any module that relies on user-configuration parameters
# must import this module.
import os

from dotenv import load_dotenv

load_dotenv()

_ENV_PREFIX: str = "MULLARDOCH_"

def _get(name: str, default: str | None = None) -> str:
    return os.environ.get(f"{_ENV_PREFIX}{name}", default)

# The type of connection to the UGV01,
# one of 'remote' (http) or 'local' (serial)
CONNECTION_TYPE: str = _get("CONNECTION_TYPE", "remote")
# The remote IP address of the UGV02
CONNECTION_REMOTE_IP: str = _get("CONNECTION_REMOTE_IP")
