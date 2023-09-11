from pydantic.main import BaseModel
from app.news.model import EventTags
from datetime import datetime
from typing import List
import uuid


class Teams(BaseModel):
    title: str
    user_id: uuid.UUID


class TeamsCreate(Teams):
    class Config:
        orm_mode = True


class TeamsExpand(Teams):
    id: uuid.UUID
    user_id: list[uuid.UUID]


class TeamsUpdate(Teams):
    pass
