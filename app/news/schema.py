from fastapi import UploadFile
from pydantic.main import BaseModel
from app.news.model import EventTags
from datetime import datetime
from typing import List


class Tag_schema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class TagCreate(Tag_schema):
    pass


class NewsWithoutTag(BaseModel):
    title: str
    description: str
    image: str
    start_of_registration: datetime
    end_of_registration: datetime
    tags: List[Tag_schema] = []

    class Config:
        orm_mode = True


class News(BaseModel):
    title: str
    description: str
    image: str
    start_of_registration: datetime
    end_of_registration: datetime
    news_tags: List[str]

    class Config:
        orm_mode = True


class NewsUpdate(News):
    pass


class NewsCreate(News):
    pass


class ShowNews(NewsWithoutTag):
    pass

class TagShow(Tag_schema):
    id: int