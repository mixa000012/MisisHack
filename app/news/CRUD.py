import uuid

from sqlalchemy import select, any_, all_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.news.model import News, Tag
from app.news.schema import NewsCreate
from app.news.schema import NewsUpdate, NewsWithoutTag, Tag_schema
from app.core.db.CRUD import ModelAccessor
from sqlalchemy.dialects import postgresql
import os


class TagDoesntExist(Exception):
    pass


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
        image_dir = 'images/'  # Replace with your desired directory path

        # Create the directory if it doesn't exist
        os.makedirs(image_dir, exist_ok=True)

        # Generate a unique filename (e.g., using the user's ID)
        filename = f'image_{uuid.uuid4()}'

        # Define the full file path
        file_path = os.path.join(image_dir, filename)
        # Save the image to the file system
        image_data = bytes(obj_in.image)
        with open(file_path, 'wb') as image_file:
            image_file.write(image_data)
        news = NewsCreate(title=obj_in.title, description=obj_in.description, image=file_path,
                          start_of_registration=obj_in.start_of_registration,
                          end_of_registration=obj_in.end_of_registration, news_tags=[])

        for tag_name in obj_in.news_tags:
            tag = await db.execute(select(Tag).where(Tag.name == tag_name))
            tag = tag.scalar()
            if tag:
                news.news_tags.append(tag)
            else:
                raise TagDoesntExist
        obj_in_data = news.dict()
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_multi_news(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ):
        stmt = select(News).options(selectinload(News.news_tags)).offset(skip).limit(limit)

        team = await db.execute(stmt)
        team = team.scalars().all()

        return team

    async def create_tag(self, db: AsyncSession, name):
        # Create a new tag
        new_tag = Tag(name=name)

        # Add and commit to the database
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)
        return new_tag

    async def get_tag(self, db: AsyncSession, tag_name):
        tag = await db.execute(select(Tag).where(Tag.name == tag_name))
        return tag

    async def get_multi_tags(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ):
        stmt = select(Tag).offset(skip).limit(limit)

        team = await db.execute(stmt)
        team = team.scalars().all()

        return team


news = NewsAccessor(News)
