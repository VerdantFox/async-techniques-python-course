import asyncio
import datetime
import random

import colorama


def main() -> None:
    loop = asyncio.new_event_loop()

    t0 = datetime.datetime.now()
    print(f"{colorama.Fore.WHITE}App started.", flush=True)
    data: asyncio.Queue[tuple[int, datetime.datetime]] = asyncio.Queue()

    task1 = loop.create_task(generate_data(20, data))
    task2 = loop.create_task(generate_data(20, data))
    task3 = loop.create_task(process_data(40, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

    dt = datetime.datetime.now() - t0
    print(
        f"{colorama.Fore.WHITE}App exiting, total time: {dt.total_seconds():,.2f} sec"
    )


async def generate_data(num: int, data: asyncio.Queue) -> None:
    for i in range(1, num + 1):
        item = i * i
        await data.put((item, datetime.datetime.now()))

        print(f"{colorama.Fore.YELLOW}  -- generated item {i}", flush=True)
        await asyncio.sleep(random.random() + 0.5)


async def process_data(num: int, data: asyncio.Queue) -> None:
    processed = 0
    while processed < num:
        item = await data.get()

        processed += 1
        value, t = item
        dt = datetime.datetime.now() - t
        print(
            f"{colorama.Fore.CYAN} +++ Processed value {value} after {dt.total_seconds():,.2f} sec."
        )
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    main()
