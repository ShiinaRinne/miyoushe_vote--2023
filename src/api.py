import json
from aiohttp import ClientSession
from .model import FullAuthorList, VotesInfo, AuthorType


proxies = {
    "http": "http://localhost:10809",
}

def set_headers(new_headers: dict):
    global headers
    headers = new_headers

async def get_data_from_url(url: str, session: ClientSession) -> dict:
    async with session.get(url=url, headers=headers) as res:
        res = await res.text()
        return json.loads(res)["data"]


async def get_users_at_page(page: int, author_type: AuthorType, session: ClientSession) -> FullAuthorList:
    url = f"https://api-takumi.mihoyo.com/event/e20231115vote/full_auth_work_list?page_type=1&author_type={author_type.value}&sort_type=VoteNum&page_num={page}&page_size=15"
    result = None
    while result is None:
        result = await get_data_from_url(url, session)
    return FullAuthorList.model_validate(result)


async def get_total_users_at_type(author_type: AuthorType, session: ClientSession) -> int:
    url = f"https://api-takumi.mihoyo.com/event/e20231115vote/full_auth_work_list?page_type=1&author_type={author_type.value}&sort_type=VoteNum&page_num=1&page_size=15"
    result = None
    while result is None:
        result = await get_data_from_url(url, session)
    return result["total"]


async def get_votes_of_user(id: int, session: ClientSession) -> VotesInfo:
    url = f"https://api-takumi.mihoyo.com/event/e20231115vote/vote_info?id={id}&page_type=1"
    result = None
    while result is None:
        result = await get_data_from_url(url, session)
    return VotesInfo.model_validate(result)
