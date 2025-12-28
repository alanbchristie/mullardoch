# Functions to generate UGV02 T-commands that are transmitted to the UGV02.
# The functions in this module are used exclusively from the queue-consumer Process
# (e.g. the queue_consumer module).
import json

import requests

import config

_UVG02_SPEED_CTRL: int = 1
_UVG02_RETRIEVE_IMU_DATA: int = 126
_UGV02_RETRIEVE_CHASSIS_INFO: int = 130


def _make_request_url(ugv02_cmd: dict[str, any]) -> str:
    """Build the request URL given a UGV02 command dictionary."""
    ugv02_cmd_str: str = json.dumps(ugv02_cmd, separators=(',', ':'))
    return f"http://{config.CONNECTION_REMOTE_IP}/js?json={ugv02_cmd_str}"


def _send(ugv02_cmd: dict[str, any]) -> bool:
    try:
        response = requests.get(_make_request_url(ugv02_cmd), timeout=2.0)
    except requests.exceptions.ConnectTimeout:
        print("Command timeout")
        return False
    return response.status_code == 200 if response else False


def send_speed_control(*, left: int, right: int) -> None:
    """Given the speed of the left and right wheels (-100 to + 100) this
    function sends the appropriate speed command to the UGV02."""
    # Speeds are limited to 20-100.
    # An absolute value of less than 20 is difficult to translate to a real speed
    # due to the low-speed characteristics of DC gear motors.
    # So values 1 to 19 are uplifted to 20.
    # Limit/adjust the left value.
    if left > 100:
        left = 100
    elif left < -100:
        left = -100
    elif left < 20 and left > 0:
        left = 20
    elif left > -20 and left < 0:
        left = -20
    # Limit/adjust the right value
    if right > 100:
        right = 100
    elif right < -100:
        right = -100
    elif right < 20 and right > 0:
        right = 20
    elif right > -20 and right < 0:
        right = -20

    # Create command dictionary - speed is a float (-1.0 to +1.0)
    ugv02_cmd: dict[str, any] = {
        "T": _UVG02_SPEED_CTRL,
        "L": left / 100,
        "R": right / 100,
    }
    return _send(ugv02_cmd)

# IMU Data
# The response consists of: -
# - Wheel data (L, R)
# - Acceleration (ax, ay, az)
# - Gyroscopic data (gx, gy, gz)
# - Magnetic (mx, my, mz)
# - ? (odl, odr)
# - Voltage (decivolts i.e. 1209 is 12.09V)
