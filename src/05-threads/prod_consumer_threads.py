import datetime
import random
import threading
import time

import colorama


def main() -> None:
    t0 = datetime.datetime.now()
    print(f"{colorama.Fore.WHITE}App started.", flush=True)
    data: list[tuple[int, datetime.datetime]] = []

    threads = [
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=process_data, args=(40, data), daemon=True),
    ]
    abort_thread = threading.Thread(target=check_cancel, daemon=True)
    abort_thread.start()

    [t.start() for t in threads]
    while any(t.is_alive() for t in threads):
        [t.join(0.001) for t in threads]
        if not abort_thread.is_alive():
            print("Cancelling on your request")
            break
    # [t.join() for t in threads]

    dt = datetime.datetime.now() - t0
    print(
        f"{colorama.Fore.WHITE}App exiting, total time: {dt.total_seconds():,.2f} sec"
    )


def check_cancel():
    print(f"{colorama.Fore.RED}Press enter to cancel...")
    input()


def generate_data(num: int, data: list) -> None:
    for i in range(1, num + 1):
        item = i * i
        data.append((item, datetime.datetime.now()))

        print(f"{colorama.Fore.YELLOW}  -- generated item {i}", flush=True)
        time.sleep(random.random() + 0.5)


def process_data(num: int, data: list) -> None:
    processed = 0
    while processed < num:
        item = None
        if data:
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
