import uuid

from fastapi import Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core import store
from app.core.deps import get_db
from app.user.auth import get_current_user_from_token
from app.teams.schema import TeamsCreate
from app.user.model import User
from fastapi import HTTPException
from app.teams.model import Teams
from sqlalchemy.orm import selectinload


async def create(obj_in: TeamsCreate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(get_current_user_from_token)):
    if current_user.is_admin or current_user.is_superadmin:
        team = await store.teams.create(db=db, obj_in=obj_in)
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")
    return team


async def create_team(
        team_name: str,
        user_ids: list[uuid.UUID] = Query(..., description="List of user IDs to add to the team"),
        db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)
):
    try:
        if current_user.is_admin or current_user.is_superadmin:
            new_team = Teams(title=team_name)
            db.add(new_team)
            await db.commit()
            await db.refresh(new_team)
            # Add users to the team
            for user_id in user_ids:
                user = await store.user.get(db, user_id)
                if user and not user.team_id:
                    user.team_id = new_team.id
                else:
                    raise HTTPException(status_code=409, detail=f"User already in a team {user.email}")

            await db.commit()

            return new_team
        else:
            raise HTTPException(status_code=403, detail="Forbidden.")
        # Create a new team

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Team with this name already exists")


async def get_users_from_team(team_id: str, db: AsyncSession = Depends(get_db)):
    # Query the database to retrieve the team and its associated users
    stmt = (
        select(Teams)
        .options(selectinload(Teams.users_of_team))
        .where(Teams.id == team_id)
    )

    team = await db.execute(stmt)

    team = team.scalar()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Access the users associated with the team via the 'users_of_team' relationship
    users = team.users_of_team
    return {"team_id": team.id, "team_title": team.title, "users": [user.email for user in users]}


async def add_member(user_id: uuid.UUID, team_id: uuid.UUID, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user_from_token)):
    if current_user.is_admin or current_user.is_superadmin:
        user = await db.execute(select(User).options(selectinload(User.team)).where(User.user_id == user_id))
        team = await db.execute(select(Teams).options(selectinload(Teams.users_of_team)).where(Teams.id == team_id))
        team = team.scalar()
        user = user.scalar()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.team_id:
            raise HTTPException(status_code=409, detail=f"User already in a team {user.team.title}")

        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        # Add the user to the team's list of users (assuming one-to-many relationship)
        team.users_of_team.append(user)

        # Commit the changes to the database
        await db.commit()

        return {"message": "User added to the team successfully"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")


async def delete_member(user_id: str, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user_from_token)):
    if current_user.is_admin or current_user.is_superadmin or current_user.user_id == user_id:
        user = await db.execute(select(User).options(selectinload(User.team)).where(User.user_id == user_id))
        user = user.scalar()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.team_id:
            raise HTTPException(status_code=409, detail=f"User not in a team!")

        # Add the user to the team's list of users (assuming one-to-many relationship)
        user.team_id = None

        # Commit the changes to the database
        await db.commit()

        return {"message": "User deleted from the team successfully"}
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")


async def get_multi(skip, limit, db: AsyncSession = Depends(get_db)):
    return await store.teams.get_multi(db=db, skip=skip, limit=limit)
