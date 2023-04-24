from uuid import UUID

from schemas import User

from .base import BaseRepository, InterfaceRepository


class UserRepository(BaseRepository, InterfaceRepository):

    def list(self, company_id: UUID):
        return self.db.query(User).filter(User.company_id == company_id).all()

    def show(self, id: UUID):
        return self.db.query(User).filter(User.id == id).first()
