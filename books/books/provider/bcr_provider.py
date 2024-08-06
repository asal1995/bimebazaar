import httpx
from books.core.config import config
import aiohttp


async def get_comment_and_rating(book_id: int, env: config):
    headers = {"x-service-key": env.service_key}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'{env.bcr_url}/cr/stats/{book_id}/') as response:
            response.raise_for_status()
            return await response.json()
