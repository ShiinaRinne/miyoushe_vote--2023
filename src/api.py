from aiohttp import ClientSession
from .model import FullAuthorList, VotesInfo, AuthorType


proxies = {
    "http": "http://localhost:10809",
}

def set_headers(new_headers: dict):
    global headers
    headers = new_headers

async def get_data_from_url(url: str, session: ClientSession) -> dict:
    result = None
    while result is None:
        async with session.get(url=url, headers=headers) as res:
            result = (await res.json())["data"]
            
    return result


async def get_users_at_page(page: int, author_type: AuthorType, session: ClientSession) -> FullAuthorList:
    url = f"https://api-takumi.mihoyo.com/event/e20231115vote/full_auth_work_list?page_type=1&author_type={author_type.value}&sort_type=VoteNum&page_num={page}&page_size=15"
    return FullAuthorList.model_validate(await get_data_from_url(url, session))


async def get_total_users_at_type(author_type: AuthorType, session: ClientSession) -> int:
    url = f"https://api-takumi.mihoyo.com/event/e20231115vote/full_auth_work_list?page_type=1&author_type={author_type.value}&sort_type=VoteNum&page_num=1&page_size=15"
    return (await get_data_from_url(url, session))["total"]


async def get_votes_of_user(id: int, session: ClientSession) -> VotesInfo:
    url = f"https://api-takumi.mihoyo.com/event/e20231115vote/vote_info?id={id}&page_type=1"
    return VotesInfo.model_validate(await get_data_from_url(url, session))
