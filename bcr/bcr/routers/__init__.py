from fastapi import APIRouter
from bcr.routers.bookmark_endpoint import route as bookmark_route
from bcr.routers.comment_rate_endpoint import route as comment_route

route = APIRouter()

route.include_router(bookmark_route, prefix="/bookmark", tags=["book Mark"])
route.include_router(comment_route, prefix="/cr", tags=["comment manager"])
