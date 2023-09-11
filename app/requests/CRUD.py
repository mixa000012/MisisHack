from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db.CRUD import ModelAccessor
from app.requests.model import Request
from app.requests.schema import RequestCreate, RequestUpdate


class RequestsAccessor(ModelAccessor[Request, RequestCreate, RequestUpdate]):
    async def create(self, db: AsyncSession, *, obj_in):
        db_obj = self.model(**obj_in)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


requests = RequestsAccessor(Request)
