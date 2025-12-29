"""Functions to generate UGV02 T-commands that are transmitted to the UGV02.
The functions in this module are used exclusively from the queue-consumer Process
(e.g. the queue_consumer module)."""

import json
from typing import Any

import requests
from config import CONNECTION_REMOTE_IP
from message import Led, Screen, Speed

# UGV02 command IDs ("T" values)
_UVG02_RESTORE_OLED_SCREEN: int = -3
_UVG02_SPEED_CTRL: int = 1
_UVG02_OLED_SCREEN_CTRL: int = 3
_UVG02_RETRIEVE_IMU_DATA: int = 126
_UGV02_RETRIEVE_CHASSIS_INFO: int = 130
_UVG02_LED_CTRL: int = 132

# Information about the OLED screen
_UGV02_OLED_SCREEN_LINES: int = 4
_UGV02_OLED_SCREEN_LINE_LENGTH: int = 21

# Maximum and minimum non-zero speed control values
# Speed is limited to a maximum of 200 in either direction.
# Also small value of less than 20 is difficult to translate
# to a real speed due to the low-speed characteristics of DC gear motors.
# So values 1 to 19 are uplifted to 20.
_UGV02_ABS_SPEED_MAX: int = 200
_UGV02_ABS_SPEED_MIN: int = 20


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
    """Given the speed of the left and right wheels (m/s x 100) this
    function sends the appropriate speed command to the UGV02.

    Speed is limited to a maximum value in either direction.
    Also small value s are difficult to translate
    to a real speed due to the low-speed characteristics of DC gear motors."""

    # Limit/uplift the left value.
    left = int(msg.left)
    if left != 0:
        original_sign: int = -1 if left < 0 else 1
        left = min(left, _UGV02_ABS_SPEED_MAX, key=abs)
        left = max(left, _UGV02_ABS_SPEED_MIN, key=abs)
        if left > 0 and original_sign == -1:
            left *= original_sign

    # Limit/uplift the right value
    right = int(msg.right)
    if right != 0:
        original_sign: int = -1 if right < 0 else 1
        right = min(right, _UGV02_ABS_SPEED_MAX, key=abs)
        right = max(right, _UGV02_ABS_SPEED_MIN, key=abs)
        if right > 0 and original_sign == -1:
            right *= original_sign

    # Create command dictionary.
    # For the UGV02 we convert the speed to a float,
    # e.g. 200 -> 2.0
    ugv02_cmd: dict[str, Any] = {
        "T": _UVG02_SPEED_CTRL,
        "L": left / 100,
        "R": right / 100,
    }
    return _send(ugv02_cmd)


def send_led_control(msg: Led) -> bool:
    """Sets the voltage for the LED switches (IO4 and IO5)."""

    # The device's sub-controller board features two 12V switch interfaces,
    # (IO4 and IO5) each with two ports, totaling four ports.
    # This command allows you to set the output voltage of these ports.
    # When the value is set to 255, it corresponds to the voltage of a 3S battery.
    # By default, these ports are used to control LED lights,
    # and you can use this command to adjust the brightness of the LEDs.
    io4: int = msg.a
    io4 = min(max(io4, 0), 100)
    io4 = io4 * 255 / 100
    io4 = int(min(max(io4, 0), 255))

    io5: int = msg.b
    io5 = min(max(io5, 0), 100)
    io5 = io5 * 255 / 100
    io5 = int(min(max(io5, 0), 255))

    ugv02_cmd: dict[str, Any] = {
        "T": _UVG02_LED_CTRL,
        "IO4": io4,
        "IO5": io5,
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
            # Only process the first 4 values in the tuple/list
            if line_num >= _UGV02_OLED_SCREEN_LINES:
                return True
            # Set the OLED text if it's not None
            # Blank strings ("") clear the corresponding line.
            if line is not None:
                ugv02_cmd = {
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
