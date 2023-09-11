from enum import Enum
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime, Boolean
import uuid
from sqlalchemy import String, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.base_class import Base
from app.user.model import User


class Request(Base):
    __tablename__ = "requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    owner_id = Column(UUID, ForeignKey("users.user_id"))
