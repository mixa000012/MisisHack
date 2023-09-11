from sqlalchemy import Text
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
from sqlalchemy.orm import relationship


class EventTags(str, Enum):
    Hackathons = 'Хакатоны'
    Victories = 'Победы'
    Meetups = 'Митапы'
    Lectures = 'Лекции'
    Meetings = 'Собрания'
    Projects = 'Проекты'
    Courses = 'Курсы'
    MISIS = 'МИСИС'
    HackathonClub = 'Хакатон-клуб'
    DAMN = 'DAMN'
    CTF = 'CTF'
    GameDev = 'Геймдев'
    Robotics = 'Робототехника'
    SportsProgramming = 'Спортивное программирование'
    AiKnowledgeClubPython = 'Ai Knowledge Club Python'


news_tags = Table('news_tags', Base.metadata,
                  Column('news_id', UUID, ForeignKey('news.id')),
                  Column('tags_id', Integer, ForeignKey('tags.id'))
                  )


class News(Base):
    __tablename__ = "news"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(Text)
    image = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    start_of_registration = Column(DateTime(timezone=True))
    end_of_registration = Column(DateTime(timezone=True))
    news_tags = relationship('Tag', secondary=news_tags, backref='news', lazy='noload')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    news_ = relationship('News', secondary=news_tags, backref='tags', lazy='noload')
