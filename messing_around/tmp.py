import datetime

import httpx


def main() -> None:
    print("Starting async event loop...")
    t0 = datetime.datetime.now()
    print("before tasks")
    results = [
        download_some_async(),
        download_some_async(175),
        download_some_async(176),
        download_some_async(177),
    ]
    print("after tasks")
    dt = datetime.datetime.now() - t0
    print(f"Synchronous code run in {dt.total_seconds():,.2f} seconds.")
    print(f"{results=}")


def download_some_async(show_num: int = 174) -> int:
    """Represents an I/O bound call (perhaps to CAISO for bids)."""
    print("Downloading...", flush=True)
    url = f"https://talkpython.fm/episodes/show/{show_num}"
    resp = httpx.get(url, follow_redirects=True)
    resp.raise_for_status()
    print(f"Downloaded (more) {len(resp.text):,} characters.", flush=True)
    return resp.status_code


if __name__ == "__main__":
    main()
