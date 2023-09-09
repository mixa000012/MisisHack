from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db.CRUD import ModelAccessor
from app.user.model import User
from app.user.schema import UserCreate, UserUpdateData


class UserAccessor(ModelAccessor[User, UserCreate, UserUpdateData]):
    async def get_by_email(self, email, db: AsyncSession):
        user = await db.execute(
            select(User).where(
                User.email == email
            )
        )

        user = user.scalar()
        return user


user = UserAccessor(User)
