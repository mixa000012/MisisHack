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
from app.user import service
from app.user.auth import get_current_user_from_token
from app.user.schema import TokenData
from app.user.schema import UserShow, User_, UserFull
from app.user.schema import UserBase
from app.user.schema import UserUpdateData
from app.user.service import UserAlreadyExist
from app.user.service import UserDoesntExist
from app.user.model import User

router = APIRouter()


async def get_id():
    return randint(100000000, 900000000)


@router.post("/token")
async def login_for_token(
        form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> TokenData:
    try:
        access_token = await service.login_for_token(form_data, db)
    except UserDoesntExist:
        raise HTTPException(
            status_code=401, detail="There is no user in database with this fio"
        )
    return TokenData(access_token=access_token, token_type="bearer")


@router.post("/users")
async def create_user(obj: UserBase, db: AsyncSession = Depends(get_db)) -> UserShow:
    try:
        user = await service.create_user(obj, db)
    except UserAlreadyExist:
        raise HTTPException(status_code=409, detail="User already exists")
    return user


@router.put("/users")
async def update_user(
        current_user: User = Depends(get_current_user_from_token),
        update_data: UserUpdateData = Body(...),
        db: AsyncSession = Depends(get_db),
) -> User_:
    updated_user = await service.update_user(current_user, update_data, db)
    return updated_user


@router.delete("/")
async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    try:
        deleted_user = await service.delete_user(user_id, db, current_user)
    except UserDoesntExist:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return deleted_user


@router.patch("/admin_privilege")
async def grant_admin_privilege(
        email: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    try:
        updated_user = await service.grant_admin_privilege(email, db, current_user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return updated_user


@router.delete("/admin_privilege")
async def revoke_admin_privilege(
        email: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> UserShow:
    try:
        updated_user = await service.grant_admin_privilege(email, db, current_user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return updated_user


@router.get('/')
async def get_user(db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user_from_token)) -> UserFull:
    return await service.get_user(db, current_user)
