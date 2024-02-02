import asyncio
import datetime

import bs4
import httpx
from colorama import Fore


def main() -> None:
    t0 = datetime.datetime.now()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_title_range())
    dt = datetime.datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2f} sec.")


async def get_title_range_old_version():
    for n in range(375, 385):
        html = await get_html(n)
        title = get_title(html, n)
        print(f"{Fore.WHITE}Title found: {title}", flush=True)


async def get_title_range():
    tasks = [(n, asyncio.create_task(get_html(n))) for n in range(375, 385)]
    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(f"{Fore.WHITE}Title found: {title}", flush=True)


async def get_html(episode_number: int) -> str:
    print(f"{Fore.YELLOW}Getting HTML for episode {episode_number}", flush=True)

    url = f"https://talkpython.fm/{episode_number}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        resp.raise_for_status()
        return resp.text


def get_title(html: str, episode_number: int) -> str:
    print(f"{Fore.CYAN}Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, "html.parser")
    header = soup.select_one("h1")
    return header.text.strip() if header else "MISSING"


if __name__ == "__main__":
    main()
