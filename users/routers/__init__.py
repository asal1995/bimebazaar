from fastapi import APIRouter
from users.routers.login_endpoint import route as login_route

route = APIRouter()

route.include_router(login_route, prefix="/users", tags=["Authentication"])
