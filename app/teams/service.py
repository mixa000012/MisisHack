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


async def create(obj_in: TeamsCreate, db: AsyncSession = Depends(get_db),
                 current_user: User = Depends(get_current_user_from_token)):
    if current_user.is_admin or current_user.is_superadmin:
        team = await store.teams.create(db=db, obj_in=obj_in)
    else:
        raise HTTPException(status_code=403, detail="Forbidden.")
    return team


async def create_team(
        team_name: str,
        user_ids: list[str] = Query(..., description="List of user IDs to add to the team"),
        db: AsyncSession = Depends(get_db)
):
    try:
        # Create a new team
        new_team = Teams(title=team_name)
        db.add(new_team)
        await db.commit()
        await db.refresh(new_team)

        # Add users to the team
        for user_id in user_ids:
            user = await db.execute(select(User).where(User.user_id== user_id))
            print(user)
            if user:
                new_team.users.append(user)

        await db.commit()

        return {"message": "Team created successfully", "team_id": new_team.id}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Team with this name already exists")
