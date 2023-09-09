from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
import uuid
from sqlalchemy import String, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    password = Column(String, nullable=False)
    fio = Column(String, default=None)
    tg = Column(String, default=None)
    github = Column(String, default=None)
    course = Column(String, default=None)
    institute = Column(String, default=None)
    direction = Column(String, default=None)
    group = Column(String, default=None)
    role = Column(ARRAY(String), default=None)
    skills = Column(ARRAY(String), default=None)
    description = Column(String, default=None)
