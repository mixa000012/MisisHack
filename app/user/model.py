from enum import Enum
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime
import uuid
from sqlalchemy import String, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.base_class import Base


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


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
    roles = Column(ARRAY(String))

    team_id = Column(UUID(as_uuid=True), ForeignKey("teams.id"))
    # Добавляем отношение к команде
    team = relationship("Teams", backref="users", lazy='noload')

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, PortalRole.ROLE_PORTAL_ADMIN}

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != PortalRole.ROLE_PORTAL_ADMIN}
