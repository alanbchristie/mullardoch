# Mullardoch

![GitHub License](https://img.shields.io/github/license/alanbchristie/mullardoch)
![GitHub Release](https://img.shields.io/github/v/release/alanbchristie/mullardoch)
[![lint](https://github.com/alanbchristie/mullardoch/actions/workflows/lint.yaml/badge.svg)](https://github.com/alanbchristie/mullardoch/actions/workflows/lint.yaml)

Experimental Python code for the Waveshare [UGV02] robot.

It's important to remember that the UGV02 implements (by default) a 3-second
motion command heartbeat. For safety reasons any motion commands (any `"T":1` commands)
will automatically stop after 3 seconds (the default heartbeat period) because the
UGV02 will assume that communications have been lost. Consequently,
if you want *continuous* motion you must issue at least one motion command for
each heartbeat period.

## Contributing
The project uses: -

- [pre-commit] to enforce linting of files prior to committing them to the
  upstream repository
- [Commitizen] to enforce a [Conventional Commit] commit message format
- [Black] as a code formatter
- [Poetry] as a package manager

You **MUST** comply with these choices in order to  contribute to the project.

To get started review the pre-commit utility and the conventional commit style
and then set-up your local clone by running the following within the DevContainer: -

    pre-commit install -t commit-msg -t pre-commit

Now the project's rules will run on every commit, and you can check the
current health of your clone with: -

    pre-commit run --all-files

## Related documentation

- https://www.waveshare.com/wiki/08_Sub-controller_JSON_Command_Set
- https://spotpear.com/index/study/detail/id/1079.html
- https://www.waveshare.com/wiki/Tutorial_IX_Lidar_and_Publishing_Lidar_Topics_in_ROS2

## Loch Mullardoch
Mullardoch is a loch (major reservoir) in the Northwest Highlands of Scotland,
and is used as a collective project codename for my UGV02 software modules.

![Loch Mullardoch](./docs/images/Loch_Mullardoch_-_geograph.org.uk_-_213606.jpg)

---

[black]: https://black.readthedocs.io/en/stable
[commitizen]: https://commitizen-tools.github.io/commitizen/
[conventional commit]: https://www.conventionalcommits.org/en/v1.0.0/
[pre-commit]: https://pre-commit.com
[poetry]: https://pypi.org/project/poetry/
[ugv02]: https://www.waveshare.com/wiki/UGV02#UGV02_User_Guide
