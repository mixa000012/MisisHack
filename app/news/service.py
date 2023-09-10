from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core import store
from app.core.deps import get_db
from app.user.auth import get_current_user_from_token
from app.news.schema import NewsCreate, News, ShowNews
from app.user.model import User
from fastapi import HTTPException
from app.news.model import EventTags


async def create_new(obj_in: NewsCreate, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user_from_token)) -> ShowNews:
    if current_user.is_admin or current_user.is_superadmin:
        news = await store.news.create_news(db=db, obj_in=obj_in)
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")
    return ShowNews(title=news.title, description=news.description, end_of_registration=news.end_of_registration,
                    start_of_registration=news.start_of_registration, tags=news.news_tags, image=news.image)


async def get_multi(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> list[ShowNews]:
    news = await store.news.get_multi(db=db, skip=skip, limit=limit)
    return news


async def filter_by_tags(tags: list[EventTags], db: AsyncSession = Depends(get_db)):
    results = await store.news.filter_by_tags(tags, db)
    return results
