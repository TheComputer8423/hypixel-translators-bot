import aiohttp
from config import crowdin_api_key

headers = {"Content-Type": "application/json", "Authorization": "Bearer " + crowdin_api_key}


async def hypixel():
    url = "https://api.crowdin.com/api/v2/projects/128098/languages/progress?limit=500"
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(url) as res:
            res_json = await res.json()

    return res_json


async def quickplay():
    url = "https://api.crowdin.com/api/v2/projects/369653/languages/progress?limit=500"
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(url) as res:
            res_json = await res.json()

    return res_json


async def htb():
    url = "https://api.crowdin.com/api/v2/projects/436418/languages/progress?limit=500"
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(url) as res:
            res_json = await res.json()

    return res_json


async def sba():
    url = "https://api.crowdin.com/api/v2/projects/369493/languages/progress?limit=500"
    async with aiohttp.ClientSession(headers=headers) as s:
        async with s.get(url) as res:
            res_json = await res.json()

    return res_json
