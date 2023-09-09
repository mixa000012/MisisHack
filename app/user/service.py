import datetime
from datetime import timedelta

from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import store
from app.core.deps import get_db
from app.user.auth import auth_user
from app.user.auth import get_current_user_from_token
from app.user.schema import UserShow, User
from app.user.schema import UserCreate
from app.user.schema import UserUpdateData
from utils import settings
from utils.security import create_access_token
from utils.hashing import Hasher

class UserDoesntExist(Exception):
    pass


class UserAlreadyExist(Exception):
    pass


async def login_for_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> str:
    user = await auth_user(form_data.username, form_data.password, db)
    if not user:
        raise UserDoesntExist
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires,
    )
    return access_token


async def create_user(obj: UserCreate, db: AsyncSession = Depends(get_db)) -> UserShow:
    user = await store.user.get_by_email(obj.email, db)
    if user:
        raise UserAlreadyExist
    user = await store.user.create(
        db,
        obj_in=UserCreate(
            email=obj.email,
            password=Hasher.get_hashed_password(obj.password),
        ),
    )
    return user


async def update_user(
        current_user: User = Depends(get_current_user_from_token),
        update_data: UserUpdateData = Body(...),
        db: AsyncSession = Depends(get_db),
) -> User:
    updated_user = await store.user.update(
        db=db,
        db_obj=current_user,
        obj_in=update_data,
    )

    return updated_user
