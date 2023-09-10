from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core import store
from app.core.deps import get_db
from app.user.auth import get_current_user_from_token
from app.news.schema import NewsCreate, News
from app.user.model import User
from fastapi import HTTPException
from app.news.model import EventTags


async def create_new(obj_in: NewsCreate, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user_from_token)) -> News:
    if current_user.is_admin or current_user.is_superadmin:
        news = await store.news.create_news(db=db, obj_in=obj_in)
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")
    return news


async def get_multi(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> list[News]:
    news = await store.news.get_multi(db=db, skip=skip, limit=limit)
    for new in news:
        print(new.tags)
    return news.all()


async def filter_by_tags(tags: list[EventTags], db: AsyncSession = Depends(get_db)):
    results = await store.news.filter_by_tags(tags, db)
    return results
