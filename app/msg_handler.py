"""Handles all messages sent to the application multiprocessing message queue.
This usually results in the construction and transmission of a JSON command
to the UGV02."""

import multiprocessing as mp
from typing import NoReturn

from message import Led, Nudge, Screen, Speed
from ugv02_command import send_led_control, send_oled_screen_control, send_speed_control

# The current speed (of left and right wheels).
# Initially 0 - motionless.
_CURRENT_SPEED: Speed = Speed()


def msg_handler(msg_queue: mp.Queue) -> NoReturn:
    """Handles high-level messages that have been sent to the given queue and
    translates them sending an appropriate T-command to the UGV02 using
    functions in the UGV02 command module.

    If any command fails the queue processing stops."""
    global _CURRENT_SPEED  # pylint: disable=global-statement

    handle_messages: bool = True
    while msg := msg_queue.get():
        if handle_messages:
            success: bool = False
            if isinstance(msg, Speed):
                # Always transmit the received speed when it's given,
                # then copy to the current speed so it's re-used when we get a 'nudge'.
                _CURRENT_SPEED = msg
                success = send_speed_control(msg)
            elif isinstance(msg, Nudge):
                # Time to re-transmit the current speed
                # (to avoid the AGV02 heart-beat timeout)
                success = send_speed_control(_CURRENT_SPEED)
            elif isinstance(msg, Screen):
                success = send_oled_screen_control(msg)
            elif isinstance(msg, Led):
                success = send_led_control(msg)
            else:
                print(f"ERROR: Unknown message ({msg})")

            if not success:
                handle_messages = False
                print("Stopped handling messages")

    # We can't get here!
    assert False
