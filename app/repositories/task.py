from uuid import UUID

from schemas import Task, User

from .base import BaseRepository, InterfaceRepository


class TaskRepository(BaseRepository, InterfaceRepository):

    def list(self, company_id: UUID):
        return self.db.query(Task).join(Task.user.and_(User.company_id == company_id)).all()

    def show(self, id: UUID, company_id: UUID):
        return self.db.query(Task).join(Task.user.and_(User.company_id == company_id)).filter(Task.id == id).first()
