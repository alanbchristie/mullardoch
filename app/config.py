"""The application run-time configuration (supporting '.env').
Any module that relies on user-configuration parameters
must import this module."""

import os

from dotenv import load_dotenv

load_dotenv()

_ENV_PREFIX: str = "MULLARDOCH_"


def _get(name: str, default: str = "") -> str:
    return os.environ.get(f"{_ENV_PREFIX}{name}", default)


# The type of connection to the UGV01,
# one of 'remote' (http) or 'local' (serial)
CONNECTION_TYPE: str = _get("CONNECTION_TYPE", "remote")
# The remote IP address of the UGV02
CONNECTION_REMOTE_IP: str = _get("CONNECTION_REMOTE_IP")

# The period (seconds) between 'Nudge' messages.
# This MUST be less than the UGV02 heartbeat period of 3 seconds
# and causes speed commands to be regenerated to avoid the heartbeat timeout.
NUDGE_PERIOD_S: float = float(_get("NUDGE_PERIOD_S", "1.5"))
