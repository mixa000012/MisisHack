from pydantic.main import BaseModel
from app.news.model import EventTags
from datetime import datetime
from typing import List
import uuid


class Teams(BaseModel):
    title: str
    user_id: uuid.UUID


class TeamsCreate(Teams):
    pass


class TeamsUpdate(Teams):
    pass
