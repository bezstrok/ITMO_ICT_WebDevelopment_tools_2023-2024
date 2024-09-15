import argparse
import threading
import time


def calculate_sum(start, end) -> int:
    return sum(range(start, end))


def worker(start, end, results, i) -> None:
    results[i] = calculate_sum(start, end)


def main(workers, start, end) -> None:
    results = [0] * workers

    tasks = []

    for i in range(workers):
        tasks.append(
            threading.Thread(
                target=worker,
                args=(
                    start + i * (end - start + 1) // workers,
                    start + (i + 1) * (end - start + 1) // workers,
                    results,
                    i,
                )
            )
        )

    start_time = time.perf_counter()
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
    result = sum(results)
    end_time = time.perf_counter()

    print(f'Сумма чисел от {start} до {end}: {result}')
    print(f'Время выполнения при {workers} воркерах: {end_time - start_time:.3f} секунд')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=10)
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=1_000_000)
    args = parser.parse_args()

    main(
        workers=args.workers,
        start=args.start,
        end=args.end
    )
