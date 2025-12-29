#!/usr/bin/env python
"""The experimental application entry point."""
import contextlib
import multiprocessing as mp

from config import CONNECTION_TYPE
from message import Led, Screen, Speed
from msg_handler import msg_handler
from nudge import nudge

# For now the connection type has to be 'remote' (i.e. http)
assert CONNECTION_TYPE == "remote"

if __name__ == "__main__":

    # Create the main message queue,
    # read by the queue consumer (command executor),
    # written from the app and the nudge scheduler
    msg_queue: mp.Queue = mp.Queue()

    # Create and start the message handler
    handler: mp.Process = mp.Process(target=msg_handler, args=(msg_queue,))
    handler.start()

    # Restore the OLED screen
    msg_queue.put_nowait(Screen())

    # Switch the LEDs off
    msg_queue.put_nowait(Led())

    # Create and start the 'nudge' process.
    # This sends a Nudge message to ensure continuous speed.
    nudger: mp.Process = mp.Process(target=nudge, args=(msg_queue,))
    nudger.start()

    # Now ask the user to provide a speed value (applied to left and right)
    left: int = 0
    right: int = 0
    print("Enter speed (m/s x 100), e.g. 20 or 200...")
    print("Control left and right independently with a pair (i.e. 0,20)")
    with contextlib.suppress(KeyboardInterrupt):
        while True:
            speed = input("New speed (CTRL-C to exit): ") or "0"
            speed_items: list[str] = speed.split(",")
            if len(speed_items) == 1:
                left = speed
                right = speed
            else:
                left = speed_items[0]
                right = speed_items[1]
            speed_msg: Speed = Speed(left=int(left), right=int(right))
            msg_queue.put_nowait(speed_msg)
