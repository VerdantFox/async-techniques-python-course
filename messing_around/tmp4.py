import datetime
from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor

import httpx


def main() -> None:
    t0 = datetime.datetime.now()
    work = []
    print("Kick off threaded tasks...", flush=True)
    with PoolExecutor() as executor:
        work.append(executor.submit(download_some_threaded))
        work.append(executor.submit(download_some_threaded, 175))
        work.append(executor.submit(download_some_threaded, 176))
        work.append(executor.submit(download_some_threaded, 177))
        print("Waiting for downloads...", flush=True)
    print("Done", flush=True)
    results = [f.result() for f in work]
    print("after tasks")
    dt = datetime.datetime.now() - t0
    print(f"Synchronous code run in {dt.total_seconds():,.2f} seconds.")
    print(f"{results=}")


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
