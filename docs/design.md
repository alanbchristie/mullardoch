# Design

## Execution
The app consists of a `main.py` entry point and run-time configuration handled
by `config.py`. Configuration is via `MULLARDOCH_` environment variables or
a root-level `.env` file. In order to run the application you will need to define
the following configuration variables: -

-   `MULLARDOCH_CONNECTION_REMOTE_IP`

To run the program, which relies on Python 3.13, just run `main.py`: -

    python app/main.py

## Modules

**config.py**

The `config` module is where the application configuration variables are held.
Following [12-factor app methodology] it relies on environment variables
that the user sets, or puts into a `.env` file. Any module that requires
run-time configuration relies on `config`.

**main.py**

The experimental application entry point - the **main** program.

**message.py**

The `messages` module provides all the definitions of messages that are
transmitted on the queue. Rather than use the JSON commands (some of which
are *peculiar*) I've decided to create a high-level abstraction of the
underlying JSON command, each implemented in a Python `dataclass`.

For example, the LED control message has an `a` and `b` property,
rather than the less intuitive `IO4` and `IO5` (especially as there
is no input on these outputs!).

**msg_handler.py**

Executed as an independent **Process** this module is responsible for
handling all the messages put onto the internal multiprocessor `Queue`.
It is the sole receiver of messages and uses the ugv02_command module to
send commands to the robot in a thread-safe, synchronous manner.

**nudge.py**

Executed as an independent **Process** this module is responsible for
the regular generation of **Nudge** messages that are put onto the
multiprocessor `Queue`, and are used by the `msg_handler` to
re-send the current speed values to the robot to ensure motion is
continuous.

**ugv02_command.py**

This module, used exclusively by the `msg_handler`, translates *messages*
into their corresponding UGV02 JSON command structures, while also
transmitting them to the robot.

## Operation

To ensure thread-safety operation of the UGV02 commands, all commands sent to it
are designed to originate from the `msg_handler.py` module, which runs as a separate
**Process**, reading *messages* from a `multiprocessing.Queue`. Commands therefore
guaranteed to originate from a single **Thread**.

When the app sends a command to the UGV02 a *message** (a Python `dataclass` object)
is put on the queue.

The `msg_handler`, being the sole receiver of messages, deals with each message
synchronously, calling functions in the `ugv02_command` module to translate the
`dataclass` object and send it to the UGV02 using the JSON string expected by the robot.

Continuous motion requires the regular reception of speed commands. To accomplish this
the `msg_handler` re-sends the most recent speed values (which it caches). As it
simply reacts to messages received on the queue it relies on a `nudge` module,
which also runs as an independent **Process**, to put regular **Nudge** messages
on the queue. The `msg_handler` responds to these messages by re-sending the most recent
speed value to the UGV02.

In summary, the app sends speed messages to the robot via a queue.
Independent processes (the `msg_handler` and `nudge`) ensure that messages are
handled safely and sent to the robot while any speed changes result in continuous motion.

---

[12-factor app methodology]: https://en.wikipedia.org/wiki/Twelve-Factor_App_methodology
