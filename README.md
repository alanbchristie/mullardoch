# Mullardoch

![GitHub License](https://img.shields.io/github/license/alanbchristie/mullardoch)

Experimental Python code for the Waveshare UGV02 robot.

It's important to remember that the UGV02 implements (by default) a 3-second
motion command heartbeat. Any motion commands (`"T":1` commands) will automatically
stop after 3 seconds, for safety - as the UGV02 will assume that
communications have been lost. Consequently, if you want continuous motion
you must repeatedly issue at least one motion command every 3 seconds.

## Lock Mullardoch
Mullardoch is a loch (major reservoir) in the Northwest Highlands of Scotland,
and is used as a collective project codename for my UGV02 software modules.

![Loch Mullardoch](./docs/images/Loch_Mullardoch_-_geograph.org.uk_-_213606.jpg)
