from sqlalchemy import select, any_, all_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.news.model import News, Tag
from app.news.schema import NewsCreate
from app.news.schema import NewsUpdate, NewsWithoutTag, Tag_schema
from app.core.db.CRUD import ModelAccessor
from sqlalchemy.dialects import postgresql


class NewsAccessor(ModelAccessor[News, NewsCreate, NewsUpdate]):
    async def filter_by_tags(self, tags, db: AsyncSession):
        tags = [i.value for i in tags]
        stmt = (
            select(News).options(selectinload(News.news_tags))
            .join(News.news_tags)  # Join the News and NewsTags tables
            .where(Tag.name.in_(tags))  # Filter by tag names
        )
        results = await db.execute(stmt)
        return results.scalars().all()

    async def create_news(self, db: AsyncSession, obj_in: NewsCreate):
        news = NewsCreate(title=obj_in.title, description=obj_in.description, image=obj_in.image,
                          start_of_registration=obj_in.start_of_registration,
                          end_of_registration=obj_in.end_of_registration, news_tags=[])
        for tag_id in obj_in.news_tags:
            tag = await db.get(Tag, tag_id)
            if tag:
                news.news_tags.append(tag)
        obj_in_data = news.dict()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ):
        stmt = select(News).options(selectinload(News.news_tags)).offset(skip).limit(limit)

        team = await db.execute(stmt)
        team = team.scalars().all()

        return team


news = NewsAccessor(News)
