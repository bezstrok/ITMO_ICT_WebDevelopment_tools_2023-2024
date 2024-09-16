from urllib.parse import urljoin

import aiohttp


__all__ = ["get_usernames_from_github"]

_api_github_url = "https://api.github.com"


async def get_usernames_from_github(page: int, *, client_session: aiohttp.ClientSession) -> list[str]:
    url = urljoin(_api_github_url, "/users")
    per_page = 30
    since = page * per_page

    async with client_session.get(url, params=dict(since=since, per_page=per_page)) as response:
        users = await response.json()

    return [user["login"] for user in users]
