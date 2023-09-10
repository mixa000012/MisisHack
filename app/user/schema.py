from enum import Enum
import uuid
from pydantic import EmailStr, validator
import re
from pydantic.main import BaseModel


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    roles: list[PortalRole]


class UserUpdateData(BaseModel):
    fio: str
    tg: str
    github: str
    course: str
    institute: str
    direction: str
    group: str
    role: list[str]
    skills: list[str]
    description: str

    @validator("tg")
    def validate_telegram_username(cls, value):
        # Telegram usernames should start with @ and can only contain letters, numbers, and underscores.
        if not re.match(r'^@[\w]+$', value):
            raise ValueError("Invalid Telegram username")
        return value

    @validator("github")
    def validate_github_url(cls, value):
        # GitHub URLs should match a pattern similar to https://github.com/username
        github_pattern = r'^https:\/\/github\.com\/[a-zA-Z0-9-]+$'
        if not re.match(github_pattern, value):
            raise ValueError("Invalid GitHub URL")
        return value

    @validator("course")
    def validate_course(cls, value):
        valid_courses = {"1", "2", "3", "4", "5", "6", "выпускник"}
        if value not in valid_courses:
            raise ValueError("Invalid course")
        return value


class User_(UserUpdateData):
    user_id: uuid.UUID
    email: EmailStr

    class Config:
        orm_mode = True


class UserShow(BaseModel):
    user_id: uuid.UUID
    email: EmailStr

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    access_token: str
    token_type: str
