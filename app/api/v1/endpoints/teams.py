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
from app.teams import service
from app.user.auth import get_current_user_from_token
from app.user.schema import TokenData
from app.user.schema import UserShow, User_
from app.user.schema import UserBase
from app.user.schema import UserUpdateData
from app.user.service import UserAlreadyExist
from app.user.service import UserDoesntExist
from app.user.model import User
from app.teams.schema import TeamsCreate

router = APIRouter()


@router.post('/')
async def create_team(user_ids: list[str], team_name: str, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user_from_token)):
    return await service.create_team(team_name, user_ids, db, current_user)


@router.get('/')
async def get_users(team_id: str, db: AsyncSession = Depends(get_db)):
    return await service.get_users_from_team(team_id, db)


@router.post('/add')
async def add_member(user_id: str, team_id: str, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user_from_token)):
    return await service.add_member(user_id, team_id, db, current_user)


@router.delete('/')
async def delete_member(user_id: str, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    return await service.delete_member(user_id, db, current_user)
