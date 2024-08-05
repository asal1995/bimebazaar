import httpx
from admin.schemas.book_schema import BookCreate
from admin.core.config import config


class BookProvider:
    def __init__(self):
        self.headers = {"x-service-key": config.service_key}
        self.base_url = config.book_url

    async def create_book(self, book: BookCreate):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.base_url.strip('/')}/", json=book.model_dump(), headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def update_book(self, book: BookCreate, book_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url=f"{self.base_url.strip('/')}/{book_id}/", json=book.model_dump(), headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def delete_book(self, book_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url=f"{self.base_url.strip('/')}/{book_id}/", headers=self.headers
            )
            response.raise_for_status()
            return response.json()
