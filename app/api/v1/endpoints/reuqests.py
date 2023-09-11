from random import randint
from uuid import UUID
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.core.deps import get_db
from app.requests import service
from app.user.auth import get_current_user_from_token
from app.user.schema import TokenData
from app.user.schema import UserShow, User_, UserFull
from app.user.schema import UserBase
from app.user.schema import UserUpdateData
from app.user.service import UserAlreadyExist
from app.user.service import UserDoesntExist
from app.user.model import User
from app.requests.schema import RequestBase, RequestCreate, RequestInDB

router = APIRouter()


@router.get('/')
async def get_request(id: str, db: AsyncSession = Depends(get_db)) -> RequestInDB:
    return await service.get_request(id, db)


@router.post('/')
async def create_request(obj_in: RequestCreate, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user_from_token)) -> RequestInDB:
    return await service.create_request(db=db, obj_in=obj_in, current_user=current_user)
