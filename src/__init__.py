import time
import openpyxl
import aiohttp
import asyncio
from typing import Dict, List

from .api import *
from .model import *

sheet = openpyxl.Workbook()
sheet.remove(sheet['Sheet'])

async def save(headers, max_gather:int = 4):
    set_headers(headers)
    
    all_author_list:Dict[str,List[AuthorInfo]] = {}
    sem = asyncio.Semaphore(max_gather)
    async with aiohttp.ClientSession() as session:
        for t in AuthorType:
            current_sheet = sheet.create_sheet(t.value)
            current_sheet.append(['Nickname', 'Vote Num Gap', 'Timestamp'])
            
            total = await get_total_users_at_type(t, session)
            
            tasks = [get_users_at_page(page, t, session) for page in range(1, total//15 + 1)]
            results = await asyncio.gather(*(sem_coro(sem, task) for task in tasks))
            
            author_info_list:List[AuthorInfo] = []
            for result in results:
                author_info_list.extend(result.full_author_list)
            
            all_author_list[t.value] = author_info_list
            
        
        for k,v in all_author_list.items():
            current_sheet = sheet[k]
            print(f"正在获取{k}分区的投票信息")
            
            tasks = [get_votes_of_user(user.aid, session) for user in v]
            results = await asyncio.gather(*(sem_coro(sem, task) for task in tasks))
            
            for user, vote_info in zip(v, results):
                current_sheet.append([user.nickname, vote_info.vote_num_gap, time.time()])
                print(f"\t{user.nickname} {vote_info.vote_num_gap}")
            
    
    sheet.save("temp.xlsx")


async def sem_coro(sem, coro):
    async with sem:
        return await coro


def calculate(file_name):
    temp = openpyxl.load_workbook("temp.xlsx")
    vote = openpyxl.Workbook()
    vote.remove(vote["Sheet"])

    for sheet in temp.worksheets:
        vote.create_sheet(sheet.title)
        vote[sheet.title].append(["Nickname", "total", "Gap"])

        user_info = []

        for row in sheet.iter_rows(min_row=2):
            user_info.append(
                (row[0].value, row[1].value, row[2].value)
            )  # nickname, gap, timestamp

        user_info.reverse()
        result_list = []
        for i in range(len(user_info)):
            user_info[i] = (
                user_info[i][0],
                0 if i == 0 else user_info[i - 1][2] + user_info[i - 1][1],
                user_info[i][1],
            )

            result_list.append(user_info[i])

        for i in result_list[::-1]:
            vote[sheet.title].append(i)

    vote.save(f"{file_name}.xlsx")
