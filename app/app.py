import config
import asyncio
import json
import urllib.parse

import aiohttp

print(f"Controlling UGV02 at {config.CONNECTION_REMOTE_IP}")

_UVG02_SPEED_CTRL: int = 1
_UVG02_RETRIEVE_IMU_DATA: int = 126

ugv02_cmd_timeout = aiohttp.ClientTimeout(total=4)

def make_request(ugv02_cmd: dict[str, any]) -> str:
    ugv02_cmd_str: str = json.dumps(ugv02_cmd, separators=(',', ':'))
    return f"http://{config.CONNECTION_REMOTE_IP}/js?json={ugv02_cmd_str}"


async def main():

    async with aiohttp.ClientSession(timeout=ugv02_cmd_timeout) as session:

        # IMU Data
        ugv02_cmd: dict[str, Any] = {"T": _UVG02_RETRIEVE_IMU_DATA}
        async with session.get(make_request(ugv02_cmd)) as ugv02_response:

            response_body = await ugv02_response.text()
            if response_body and response_body != "null":
                print(response_body)

        # FORWARD (0.05)
        ugv02_cmd: dict[str, Any] = {"T": _UVG02_SPEED_CTRL,
                                     "L": 0.05,
                                     "R": 0.05}
        async with session.get(make_request(ugv02_cmd)) as ugv02_response:

            response_body = await ugv02_response.text()
            if response_body and response_body != "null":
                print(response_body)

        # IMU Data
        for _ in range(10):
            ugv02_cmd: dict[str, Any] = {"T": 130}
            async with session.get(make_request(ugv02_cmd)) as ugv02_response:

                response_body = await ugv02_response.text()
                if response_body and response_body != "null":
                    print(response_body)

            await asyncio.sleep(1)


asyncio.run(main())
