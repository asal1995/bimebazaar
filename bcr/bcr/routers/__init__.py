from fastapi import APIRouter
from books.routers.books_endpoint import route as book_route

route = APIRouter()

route.include_router(book_route, prefix="/books", tags=["book manager"])
