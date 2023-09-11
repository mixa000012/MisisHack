from enum import Enum
from datetime import timedelta
from uuid import UUID
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import store
from app.core.deps import get_db
from app.user.auth import auth_user
from app.user.auth import get_current_user_from_token
from app.user.schema import UserShow, User_, UserBase
from app.user.schema import UserCreate
from app.user.schema import UserUpdateData
from utils import settings
from utils.security import create_access_token
from app.requests.schema import RequestBase, RequestCreate, RequestInDB
from app.user.model import User
from app.requests.model import Request


async def get_request(id: str, db: AsyncSession = Depends(get_db)) -> RequestInDB:
    return await store.requests.get(db, id)


async def create_request(obj_in: RequestCreate, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)):
    obj_in_dict = obj_in.dict()
    obj_in_dict["owner_id"] = current_user.user_id
    return await store.requests.create(db, obj_in=obj_in_dict)
