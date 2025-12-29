"""The high-level messages sent to the application queue.
There are multiple transmitters and one receiver."""

from dataclasses import dataclass


@dataclass
class Led:
    """An LED message, used to set the voltage available on the
    two 12V switch interfaces (IO4 and IO5). Values in this class
    are percentages (0-100) with 'a' representing IO4 and 'b'
    representing IO5. A value of 100% corresponds to the battery voltage
    (12v). Values less then 0 are interpreted as 0. Values greater than
    100 are interpreted as 100.

    There isn't a linear relationship between input value and voltage.
    For example, to set IO4 and IO5 to approximately half the voltage
    you need an input value of 28%."""

    # Empirical (no load) input/output characteristics: -
    #
    # 100% = 11.05v
    #  90% = 10.89v
    #  80% = 10.43v
    #  70% =  9.67v
    #  60% =  8.77v
    #  50% =  7.75v
    #  40% =  6.75v
    #  30% =  5.66v
    #  20% =  4.60v
    #  10% =  3.67v
    #   0% =   0.0v

    a: int = 0
    b: int = 0


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
