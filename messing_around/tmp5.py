import asyncio
import datetime
from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor

import httpx


def main() -> None:
    print("Starting async event loop...", flush=True)
    t0 = datetime.datetime.now()

    # First run the async code
    results_async = asyncio.run(
        run_async_tasks(
            download_some_async(),
            download_some_async(175),
            download_some_async(176),
            download_some_async(177),
        )
    )

    # Separately run the threaded code
    results_threaded = run_threaded_tasks(
        (download_some_threaded,),
        (download_some_threaded, 175),
        (download_some_threaded, 176),
        (download_some_threaded, 177),
    )
    dt = datetime.datetime.now() - t0
    print(f"Asyncio code run in {dt.total_seconds():,.2f} seconds.", flush=True)
    print(f"{results_async=}", flush=True)
    print(f"{results_threaded=}", flush=True)
    print(results_async == results_threaded, flush=True)


async def run_async_tasks(*coroutines):
    """Run async tasks gathered with asyncio.gather."""
    tasks = asyncio.gather(*coroutines)
    print("Done gathering tasks. Kicking off tasks...", flush=True)
    results = await tasks
    print("Done gathering results.", flush=True)
    return results


def run_threaded_tasks(*tasks) -> list[int]:
    print("Kick off threaded tasks...", flush=True)
    with PoolExecutor() as executor:
        work = [executor.submit(*task) for task in tasks]
        print("Waiting for downloads...", flush=True)
    print("Done", flush=True)
    return [f.result() for f in work]


async def download_some_async(show_num: int = 174) -> int:
    """Represents an I/O bound call (perhaps to CAISO for bids)."""
    print("Downloading...", flush=True)
    url = f"https://talkpython.fm/episodes/show/{show_num}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
    print(f"Downloaded (more) {len(resp.text):,} characters.", flush=True)
    return resp.status_code


def download_some_threaded(show_num: int = 174) -> int:
    """Represents an I/O bound call (perhaps to CAISO for bids)."""
    print("Downloading...", flush=True)
    url = f"https://talkpython.fm/episodes/show/{show_num}"
    resp = httpx.get(url, follow_redirects=True)
    resp.raise_for_status()
    print(f"Downloaded (more) {len(resp.text):,} characters.", flush=True)
    return resp.status_code


if __name__ == "__main__":
    main()
