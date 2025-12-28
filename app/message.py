"""The high-level messages sent to the application queue.
There are multiple transmitters and one receiver."""

from dataclasses import dataclass


@dataclass
class Nudge:
    """A Nudge message, generated exclusively by the 'nudge' process.
    Used to ensure continuous speed."""

    ordinal: int | None = None


@dataclass
class Speed:
    """Speed definition. Left and right are integers from -100 to +100."""

    left: int = 0
    right: int = 0
