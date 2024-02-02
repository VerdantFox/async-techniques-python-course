import asyncio
import datetime
import math

import aiohttp
import requests
from unsync import unsync


def main():
    t0 = datetime.datetime.now()

    tasks = [
        compute_some(),
        compute_some(2),
        compute_some(3),
        download_some_async(),
        download_some_async(175),
        download_some_more_sync(92),
        download_some_more_sync(93),
        wait_some(),
        wait_some(),
        wait_some(),
        wait_some(),
    ]
    results = [t.result() for t in tasks]

    dt = datetime.datetime.now() - t0
    print(f"Unsync version done in {dt.total_seconds():,.2f} seconds.")
    print(results)


@unsync(cpu_bound=True)
def compute_some(arg: int = 1):
    result = 0
    for _ in range(1, 10_000_000):
        result += math.sqrt(25**25 + 0.01)
    return result


@unsync()
async def download_some_async(show_num: int = 174):
    print("Downloading...")
    url = f"https://talkpython.fm/episodes/show/{show_num}/coming-into-python-from-another-industry-part-2"
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            text = await resp.text()
    print(f"Downloaded (more) {len(text):,} characters.")
    return text


@unsync()
def download_some_more_sync(show_num: int):
    print("Downloading more ...")
    url = (
        f"https://pythonbytes.fm/episodes/show/{show_num}/will-your-python-be-compiled"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    text = resp.text

    print(f"Downloaded {len(text):,} characters.")
    return text


@unsync()
async def wait_some():
    print("Waiting...")
    for _ in range(1, 1000):
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    main()
