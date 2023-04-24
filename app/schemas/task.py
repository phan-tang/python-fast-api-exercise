import enum
from sqlalchemy import Column, String, Enum, Numeric, Uuid, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from .base_entity import BaseEntity


class TaskStatus(enum.Enum):
    CLOSED = 'C'
    ACTIVE = 'A'
    NEW = 'N'


class Task(Base, BaseEntity):
    __tablename__ = 'tasks'

    user_id = Column(Uuid, ForeignKey('users.id'), nullable=False)
    summary = Column(String)
    description = Column(String)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NEW)
    priority = Column(Numeric, nullable=False, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship('User')
