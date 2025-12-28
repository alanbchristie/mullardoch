"""The high-level messages sent to the application queue.
There are multiple transmitters and one receiver."""

from dataclasses import dataclass


@dataclass
class Nudge:
    """A Nudge message, generated exclusively by the 'nudge' process.
    Used to ensure continuous speed."""

    ordinal: int | None = None


@dataclass
class Screen:
    """A message to put items in the 4-line OLED UGV02 rear display.
    A text entry that is None is not modified. Each line is limited
    to 21 characters and is truncated before display to avoid line-wrap.

    If all the text lines are None (i.e. it's the default object) the display is reset.
    """

    text: tuple = (None, None, None, None)


@dataclass
class Speed:
    """Speed definition. Left and right are integers from -100 to +100."""

    left: int = 0
    right: int = 0
