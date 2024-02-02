import asyncio
import datetime

import httpx


def main() -> None:
    print("Starting async event loop...", flush=True)
    t0 = datetime.datetime.now()
    results = asyncio.run(
        run_tasks(
            download_some_async(),
            download_some_async(175),
            download_some_async(176),
            download_some_async(177),
        )
    )
    dt = datetime.datetime.now() - t0
    print(f"Asyncio code run in {dt.total_seconds():,.2f} seconds.", flush=True)
    print(f"{results=}", flush=True)


async def run_tasks(*coroutines):
    """Run async tasks gathered with asyncio.gather.

    Alternatively could run with asyncio.create_task:

    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(c) for c in coroutines]
    results = [await t for t in tasks]
    return results
    """
    tasks = asyncio.gather(*coroutines)
    print("Done gathering tasks. Kicking off tasks...", flush=True)
    results = await tasks
    print("Done gathering results.", flush=True)
    return results


async def download_some_async(show_num: int = 174) -> int:
    """Represents an I/O bound call (perhaps to CAISO for bids)."""
    print("Downloading...", flush=True)
    url = f"https://talkpython.fm/episodes/show/{show_num}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
    print(f"Downloaded (more) {len(resp.text):,} characters.", flush=True)
    return resp.status_code


if __name__ == "__main__":
    main()
