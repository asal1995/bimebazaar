from fastapi import APIRouter
from admin.routers.book_pro_endpoint import route as book_pro_route

route = APIRouter()

route.include_router(book_pro_route, prefix="/admin", tags=["book provider"])
