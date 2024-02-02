import datetime

import httpx
import unsync


def main() -> None:
    t0 = datetime.datetime.now()

    print("Kicking off tasks...", flush=True)
    tasks = [
        download_some_async(),
        download_some_async(175),
        download_some_async(176),
        download_some_async(177),
        download_some_threaded(),
        download_some_threaded(175),
        download_some_threaded(176),
        download_some_threaded(177),
    ]
    print("Tasks all kicked off.", flush=True)
    print("Waiting for results...", flush=True)
    results = [t.result() for t in tasks]
    print("Done gathering results.", flush=True)
    dt = datetime.datetime.now() - t0
    print(f"{results=}", flush=True)
    print(f"Unsync code run in {dt.total_seconds():,.2f} seconds.", flush=True)


@unsync.unsync
async def download_some_async(show_num: int = 174) -> int:
    """Represents an I/O bound call (perhaps to CAISO for bids)."""
    print("Downloading...", flush=True)
    url = f"https://talkpython.fm/episodes/show/{show_num}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
    print(f"Downloaded (more) {len(resp.text):,} characters.", flush=True)
    return resp.status_code


@unsync.unsync
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
