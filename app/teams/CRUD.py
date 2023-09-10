from sqlalchemy import select, any_
from sqlalchemy.ext.asyncio import AsyncSession

from app.teams.model import Teams
from app.teams.schema import TeamsCreate, TeamsUpdate
from app.core.db.CRUD import ModelAccessor


class TeamsAccessor(ModelAccessor[Teams, TeamsCreate, TeamsUpdate]):
    pass


teams = TeamsAccessor(Teams)
