import multiprocessing as mp
from typing import NoReturn

import message
from ugv02_command import send_speed_control

# The current speed (of left and right wheels).
# Initially 0 - motionless.
_CURRENT_SPEED: message.Speed = message.Speed()


def msg_handler(msg_queue: mp.Queue) -> NoReturn:
    """Handles high-level messages that have been sent to the given queue and
    translates them sending an appropriate T-command to the UGV02 using
    functions in the UGV02 command module.

    If any command fails the queue processing stops."""
    global _CURRENT_SPEED

    stop: bool = False
    while msg := msg_queue.get():
        if isinstance(msg, message.Speed):
            # Always transmit the received speed when it's given,
            # then copy to the current speed so it's re-used when we get a 'nudge'.
            _CURRENT_SPEED = msg
            if not send_speed_control(left=msg.left, right=msg.right):
                stop = True
        elif isinstance(msg, message.Nudge):
            # Time to re-transmit the current speed
            # (to avoid the AGV02 heart-beat timeout)
            if not send_speed_control(left=_CURRENT_SPEED.left, right=_CURRENT_SPEED.right):
                stop = True

        if stop:
            break

    print("Stopped handling messages")
