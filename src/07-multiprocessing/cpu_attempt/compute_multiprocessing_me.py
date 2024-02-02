import datetime
import math
import multiprocessing


def main():
    do_math(1)

    t0 = datetime.datetime.now()

    # do_math(num=30000000)
    print(f"Doing math on {multiprocessing.cpu_count():,} processors.")

    processor_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool()

    tasks = []
    for n in range(1, processor_count + 1):
        args = (
            30_000_000 * (n - 1) / processor_count,
            30_000_000 * n / processor_count,
        )
        task = pool.apply_async(do_math, args)
        tasks.append(task)
    pool.close()
    pool.join()

    dt = datetime.datetime.now() - t0

    print(f"Done in {dt.total_seconds():,.2f} sec.")
    print("our results: ")
    for t in tasks:
        print(t.get())


def do_math(start=0, num=10):
    pos = start
    k_sq = 1000 * 1000
    average = 0
    while pos < num:
        pos += 1
        val = math.sqrt((pos - k_sq) * (pos - k_sq))
        average += val / num

    return int(average)


if __name__ == "__main__":
    main()
