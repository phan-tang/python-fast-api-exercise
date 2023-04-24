from uuid import UUID

from .base import BaseRepository, InterfaceRepository

from schemas import User


class AdminRepository(BaseRepository, InterfaceRepository):

    def list(self):
        return self.db.query(User).filter(User.is_admin == True).all()

    def show(self, id: UUID):
        return self.db.query(User).filter(User.id == id and User.is_admin == True).first()
