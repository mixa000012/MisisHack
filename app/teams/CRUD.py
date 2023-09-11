from sqlalchemy import select, any_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.teams.model import Teams
from app.teams.schema import TeamsCreate, TeamsUpdate
from app.core.db.CRUD import ModelAccessor


class TeamsAccessor(ModelAccessor[Teams, TeamsCreate, TeamsUpdate]):
    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ):
        teams_with_user_ids = []
        stmt = select(Teams).options(selectinload(Teams.users_of_team)).offset(skip).limit(limit)
        team = await db.execute(stmt)
        team = team.scalars().all()
        for team in team:
            team_with_user_ids = {
                "id": team.id,
                "title": team.title,  # Include other team attributes as needed
                "user_id": [user.user_id for user in team.users_of_team],
            }
            teams_with_user_ids.append(team_with_user_ids)
        return teams_with_user_ids


teams = TeamsAccessor(Teams)
