import threading
import time


def main():
    threads = [
        threading.Thread(target=greeter, args=("Teddy", 10), daemon=True),
        threading.Thread(target=greeter, args=("Sarah", 5), daemon=True),
        threading.Thread(target=greeter, args=("Zoey", 2), daemon=True),
        threading.Thread(target=greeter, args=("Mark", 11), daemon=True),
    ]
    [t.start() for t in threads]

    print("This is other work.")

    [t.join(timeout=1) for t in threads]

    print("Done")


def greeter(name: str, times: int) -> None:
    for n in range(times):
        print(f"{n}. hello there {name}")
        time.sleep(1)


if __name__ == "__main__":
    main()
