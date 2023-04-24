from fastapi import Depends
from uuid import UUID
from datetime import datetime

from schemas import Task
from models import TaskModel

from repositories import TaskRepository
from .base import BaseService


class TaskService(BaseService):
    repository: TaskRepository

    def __init__(self, repository: TaskRepository = Depends()) -> None:
        self.repository = repository

    def list(self, company_id: UUID):
        return self.repository.list(company_id)

    def show(self, id: UUID, company_id: UUID):
        return self.repository.show(id, company_id)

    def create(self, request: TaskModel):
        task = Task(**dict(request))
        task.created_at = datetime.utcnow()
        return self.repository.create(task)

    def update(self, id: UUID, request: TaskModel):
        task = Task(**dict(request))
        task.id = id
        task.updated_at = datetime.utcnow()
        return self.repository.update(task)

    def delete(self, task: Task):
        return self.repository.delete(task)
