from uuid import UUID

from schemas import User

from .base import BaseRepository, InterfaceRepository


class UserRepository(BaseRepository, InterfaceRepository):

    def list(self, company_id: UUID, params):
        query = self.db.query(User)
        query = self.filter(query, User, params)
        query = self.search(query, User, params)
        query = self.sort(query, User, params)
        query = query.filter(User.company_id == company_id)
        query = self.paginate(query, params)
        return query.all()

    def show(self, id: UUID):
        return self.db.query(User).filter(User.id == id).first()
