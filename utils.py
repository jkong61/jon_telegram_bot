from aiohttp import ClientSession

async def fetch(url: str, session: ClientSession):
    async with session.get(url) as response:
        return await response.text()
