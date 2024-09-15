import argparse
import multiprocessing
import time

from . import database, request


def process_page(page: int):
    content = request.sync_get_content(page)
    usernames = [user["login"] for user in content]
    database.sync_insert(usernames)


def main(pages: int):
    tasks = [multiprocessing.Process(target=process_page, args=(page,)) for page in range(pages)]
    start = time.perf_counter()
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    end = time.perf_counter()

    print(f"Затрачено времени: {end - start:.2f} секунд для {pages} страниц")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", type=int)
    args = parser.parse_args()

    main(args.pages)
