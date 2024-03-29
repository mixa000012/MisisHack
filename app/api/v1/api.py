from fastapi import APIRouter

from app.api.v1.endpoints import user, news, teams, reuqests

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(reuqests.router, prefix="/requests", tags=["requests"])
