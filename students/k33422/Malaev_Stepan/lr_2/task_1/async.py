import argparse
import asyncio
import time


async def calculate_sum(start, end) -> int:
    return sum(range(start, end))


async def main(workers, start, end) -> None:
    tasks = []

    for i in range(workers):
        tasks.append(
            asyncio.create_task(
                calculate_sum(
                    start + i * (end - start + 1) // workers,
                    start + (i + 1) * (end - start + 1) // workers
                )
            )
        )

    start_time = time.perf_counter()
    result = sum(await asyncio.gather(*tasks))
    end_time = time.perf_counter()

    print(f'Сумма чисел от {start} до {end}: {result}')
    print(f'Время выполнения при {workers} воркерах: {end_time - start_time:.3f} секунд')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=10)
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=1_000_000)
    args = parser.parse_args()

    asyncio.run(
        main(
            workers=args.workers,
            start=args.start,
            end=args.end
        )
    )
