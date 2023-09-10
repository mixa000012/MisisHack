from random import randint
from uuid import UUID
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.news.model import EventTags
from app.core.deps import get_db
from app.news import service
from app.news.schema import NewsCreate, NewsUpdate, News, ShowNews
from app.user.model import User
from app.user.auth import get_current_user_from_token

router = APIRouter()


@router.post("/news")
async def create_new(obj: NewsCreate, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user_from_token)) -> ShowNews:
    news = await service.create_new(obj, db, current_user)
    return news


@router.get("/news")
async def get_news(skip: int, limit: int, db: AsyncSession = Depends(get_db)):
    news = await service.get_multi(db, skip, limit)
    return news


@router.post('/filter')
async def filter_news(tags: list[EventTags], db: AsyncSession = Depends(get_db)):
    return await service.filter_by_tags(tags, db)
