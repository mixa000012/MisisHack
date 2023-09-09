from enum import Enum
import uuid

from pydantic.main import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    pass


class Sex(str, Enum):
    male = "Мужчина"
    female = "Женщина"


class UserUpdateData(BaseModel):
    sex: Sex | None = None
    address: str | None = None
    survey_result: str | None = None


class UserShow(BaseModel):
    user_id: uuid.UUID
    email: str

    class Config:
        orm_mode = True


class UserShowAddress(UserBase):
    created_at: str


class TokenData(BaseModel):
    access_token: str
    token_type: str
