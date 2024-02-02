from typing import Generator

# def fib(n: int) -> list[int]:
#     nums: list[int] = []
#     current, nxt = 0, 1
#     while len(nums) < n:
#         current, nxt = nxt, current + nxt
#         nums.append(current)
#     return nums


def fib() -> Generator[int, None, None]:
    current, nxt = 0, 1
    while True:
        current, nxt = nxt, current + nxt
        yield current


if __name__ == "__main__":
    for n in fib():
        print(n, end=", ")
        if n > 1000:
            break

    print()
    print("Done")
