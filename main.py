from src import save, calculate
import time


headers = {
    "referer": "https://act.mihoyo.com/",
    "cookie": ""
}

async def main():
    await save(headers = headers, max_gather=4)
    calculate(int(time.time()))
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())