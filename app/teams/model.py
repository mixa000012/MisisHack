from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from enum import Enum
from app.core.db.base_class import Base

from sqlalchemy import Column, Table
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from app.user.model import User


class Teams(Base):
    __tablename__ = "teams"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    users_of_team = relationship("User", backref="teams", lazy='noload')

    def __init__(self, title):
        self.title = title

    def add_user(self, user):
        if len(self.users) < 5:
            self.users.append(user)
        else:
            raise Exception("The team is full.")
