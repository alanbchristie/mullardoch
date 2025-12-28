import contextlib
import multiprocessing as mp

import config
from queue_consumer import msg_handler
from nudge import nudge
from message import Speed

assert config.CONNECTION_TYPE == "remote"

if __name__ == '__main__':

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

    # Now ask the user to provide a speed value (applied to left and right)
    with contextlib.suppress(KeyboardInterrupt):
        while True:
            speed = input("New speed: ")
            speed_msg: Speed = Speed(left=int(speed), right=int(speed))
            msg_queue.put_nowait(speed_msg)
