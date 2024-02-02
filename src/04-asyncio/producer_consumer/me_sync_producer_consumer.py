import datetime
import random
import time

import colorama


def main() -> None:
    t0 = datetime.datetime.now()
    print(f"{colorama.Fore.WHITE}App started.", flush=True)
    data = []
    generate_data(20, data)
    process_data(20, data)

    dt = datetime.datetime.now() - t0
    print(
        f"{colorama.Fore.WHITE}App exiting, total time: {dt.total_seconds():,.2f} sec"
    )


def generate_data(num: int, data: list) -> None:
    for i in range(1, num + 1):
        item = i * i
        data.append((item, datetime.datetime.now()))

        print(f"{colorama.Fore.YELLOW}  -- generated item {i}", flush=True)
        time.sleep(random.random() + 0.5)


def process_data(num: int, data: list) -> None:
    processed = 0
    while processed < num:
        item = data.pop(0)
        if not item:
            time.sleep(0.01)
            continue

        processed += 1
        value, t = item
        dt = datetime.datetime.now() - t
        print(
            f"{colorama.Fore.CYAN} +++ Processed value {value} after {dt.total_seconds():,.2f} sec."
        )
        time.sleep(0.5)


if __name__ == "__main__":
    main()
