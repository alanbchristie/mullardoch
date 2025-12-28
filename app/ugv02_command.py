"""Functions to generate UGV02 T-commands that are transmitted to the UGV02.
The functions in this module are used exclusively from the queue-consumer Process
(e.g. the queue_consumer module)."""

import json
from typing import Any

import requests
from config import CONNECTION_REMOTE_IP
from message import Screen, Speed

# UGV02 command IDs ("T" values)
_UVG02_RESTORE_OLED_SCREEN: int = -3
_UVG02_SPEED_CTRL: int = 1
_UVG02_OLED_SCREEN_CTRL: int = 3
_UVG02_RETRIEVE_IMU_DATA: int = 126
_UGV02_RETRIEVE_CHASSIS_INFO: int = 130

_UGV02_OLED_SCREEN_LINES: int = 4
_UGV02_OLED_SCREEN_LINE_LENGTH: int = 21


def _make_request_url(ugv02_cmd: dict[str, Any]) -> str:
    """Build the request URL given a UGV02 command dictionary."""
    ugv02_cmd_str: str = json.dumps(ugv02_cmd, separators=(",", ":"))
    return f"http://{CONNECTION_REMOTE_IP}/js?json={ugv02_cmd_str}"


def _send(ugv02_cmd: dict[str, Any]) -> bool:
    try:
        response = requests.get(_make_request_url(ugv02_cmd), timeout=2.0)
    except requests.exceptions.ConnectTimeout:
        print("Command timeout")
        return False
    return response.status_code == 200 if response else False


def send_speed_control(msg: Speed) -> bool:
    """Given the speed of the left and right wheels (-100 to + 100) this
    function sends the appropriate speed command to the UGV02."""
    # Speeds are limited to 20-100.
    # An absolute value of less than 20 is difficult to translate to a real speed
    # due to the low-speed characteristics of DC gear motors.
    # So values 1 to 19 are uplifted to 20.
    # Limit/adjust the left value.
    left = msg.left
    if left > 100:
        left = 100
    elif left < -100:
        left = -100
    elif 0 < left < 20:
        left = 20
    elif -20 < left < 0:
        left = -20
    # Limit/adjust the right value
    right = msg.right
    if right > 100:
        right = 100
    elif right < -100:
        right = -100
    elif 0 < right < 20:
        right = 20
    elif -20 < right < 0:
        right = -20

    # Create command dictionary - speed is a float (-1.0 to +1.0)
    ugv02_cmd: dict[str, Any] = {
        "T": _UVG02_SPEED_CTRL,
        "L": left / 100,
        "R": right / 100,
    }
    return _send(ugv02_cmd)


def send_oled_screen_control(msg: Screen) -> bool:
    """Sets lines on the rear UGV02 OLED screen.
    If no lines are defined the screen display is reset."""

    if msg.text == (None, None, None, None):
        ugv02_cmd: dict[str, Any] = {
            "T": _UVG02_RESTORE_OLED_SCREEN,
        }
        if not _send(ugv02_cmd):
            return False
    else:
        for line_num, line in enumerate(msg.text):
            if line_num >= _UGV02_OLED_SCREEN_LINES:
                return True
            if line is not None:
                ugv02_cmd: dict[str, Any] = {
                    "T": _UVG02_OLED_SCREEN_CTRL,
                    "lineNum": line_num,
                    "Text": str(line)[:_UGV02_OLED_SCREEN_LINE_LENGTH],
                }
                if not _send(ugv02_cmd):
                    return False
    return True


# IMU Data
# The response consists of: -
# - Wheel data (L, R)
# - Acceleration (ax, ay, az)
# - Gyroscopic data (gx, gy, gz)
# - Magnetic (mx, my, mz)
# - ? (odl, odr)
# - Voltage (decivolts i.e. 1209 is 12.09V)
