# An APScheduler process with one 'interval' Job to nudge the
# queue consumer into regenerating Speed commands to avoid the UGV02 command heartbeat.
import multiprocessing as mp
from typing import NoReturn

from apscheduler.schedulers.blocking import BlockingScheduler

import config
from message import Nudge


def _interval_job(msg_queue: mp.Queue) -> None:
    """Just send an empty 'Nudge' message."""
    msg_queue.put_nowait(Nudge())


def nudge(msg_queue: mp.Queue) -> NoReturn:
    """Uses the APScheduler to generate a 'Nudge' message every few seconds."""
    scheduler: BlockingScheduler = BlockingScheduler()
    scheduler.add_job(
        _interval_job,
        args=[msg_queue],
        trigger='interval',
        seconds=config.NUDGE_PERIOD_S,
    )
    scheduler.start()
