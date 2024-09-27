import typing as tp

import aiohttp
import requests

url = "https://api.github.com/users"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}


def page_to_params(page: int) -> dict[str, tp.Any]:
    per_page = 30
    since = page * per_page
    return dict(since=since, per_page=per_page)


async def async_get_content(page: int) -> list[dict[str, tp.Any]]:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=page_to_params(page)) as response:
            return await response.json()


def sync_get_content(page: int) -> list[dict[str, tp.Any]]:
    response = requests.get(url, params=page_to_params(page), headers=headers)
    return response.json()
