from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional
from models import BaseUserViewModel
from schemas import TaskStatus


class TaskModel(BaseModel):
    user_id: UUID
    summary: Optional[str] = Field()
    description: Optional[str] = Field()
    status: TaskStatus = Field(default=TaskStatus.NEW)
    priority: int = Field(default=1)


class BaseTaskViewModel(BaseModel):
    id: UUID
    user_id: UUID
    summary: str | None = None
    description: str | None = None
    status: TaskStatus
    priority: int

    class Config:
        orm_mode = True


class TaskViewModel(BaseTaskViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user: BaseUserViewModel

    class Config:
        orm_mode = True
