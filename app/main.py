#!/usr/bin/env python
"""The experimental application entry point."""
import contextlib
import multiprocessing as mp

from config import CONNECTION_TYPE
from message import Screen, Speed
from nudge import nudge
from queue_consumer import msg_handler

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

    # Create and start the 'nudge' process.
    # This sends a Nudge message at least once every 3 seconds.
    nudger: mp.Process = mp.Process(target=nudge, args=(msg_queue,))
    nudger.start()

    msg = Screen()
    msg_queue.put_nowait(msg)

    # Now ask the user to provide a speed value (applied to left and right)
    left: int = 0
    right: int = 0
    print("Enter speed, e.g. 10,20 or 30...")
    with contextlib.suppress(KeyboardInterrupt):
        while True:
            speed = input("New speed (CTRL-C to exit): ")
            speed_items: list[str] = speed.split(",")
            if len(speed_items) == 1:
                left = speed
                right = speed
            else:
                left = speed_items[0]
                right = speed_items[1]
            speed_msg: Speed = Speed(left=int(left), right=int(right))
            msg_queue.put_nowait(speed_msg)
