import argparse
import asyncio
import time

from . import database, request


async def process_page(page: int):
    content = await request.async_get_content(page)
    usernames = [user["login"] for user in content]
    await database.async_insert(usernames)


async def main(pages: int):
    tasks = [process_page(page) for page in range(pages)]
    start = time.perf_counter()
    await asyncio.gather(*tasks)
    end = time.perf_counter()

    print(f"Затрачено времени: {end - start:.2f} секунд для {pages} страниц")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", type=int)
    args = parser.parse_args()

    asyncio.run(main(args.pages))
