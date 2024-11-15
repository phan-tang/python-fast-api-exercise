from uuid import UUID

from schemas import Task, User
from sqlalchemy import and_
from .base import BaseRepository, InterfaceRepository


class TaskRepository(BaseRepository, InterfaceRepository):

    def list(self, company_id: UUID, params):
        query = self.db.query(Task)
        query = self.filter(query, Task, params)
        query = self.search(query, Task, params)
        query = self.sort(query, Task, params)
        query = query.join(Task.user.and_(User.company_id == company_id))
        query = self.paginate(query, params)
        return query.all()

    def show(self, id: UUID, company_id: UUID):
        return self.db.query(Task).join(Task.user.and_(User.company_id == company_id)).filter(Task.id == id).first()

    def find_user_of_company(self, company_id: str, user_id: str):
        return self.db.query(User).filter(and_(*[User.company_id == company_id, User.id == user_id])).first()
