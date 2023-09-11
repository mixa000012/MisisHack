from enum import Enum
import uuid
from pydantic import EmailStr, validator
import re
from pydantic.main import BaseModel
from datetime import datetime


class RequestBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class RequestCreate(RequestBase):
    pass

    class Config:
        orm_mode = True




class RequestUpdate(RequestBase):
    pass


class RequestInDB(RequestBase):
    id: uuid.UUID
    status: bool
    created_at: datetime
    owner_id: uuid.UUID

    class Config:
        orm_mode = True


