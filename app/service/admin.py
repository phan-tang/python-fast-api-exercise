from fastapi import Depends, HTTPException
from datetime import datetime
from uuid import UUID

from schemas import User, get_password_hash
from models import AdminModel

from repositories import AdminRepository
from .base import BaseService


class AdminService(BaseService):
    repository: AdminRepository

    def __init__(self, repository: AdminRepository = Depends()) -> None:
        self.repository = repository
        self.uniqe_fields = ['username', 'email']

    def list(self):
        return self.repository.list()

    def show(self, id: UUID):
        return self.repository.show(id)

    def create(self, request: AdminModel):
        new_user = User(**dict(request))
        for key in self.uniqe_fields:
            self.check_username_email_exists(key, getattr(new_user, key))
        new_user.is_superadmin = False
        new_user.is_admin = True
        new_user.password = get_password_hash(request.password)
        new_user.created_at = datetime.utcnow()
        return self.repository.create(new_user)

    def update(self, old_user: User, request: AdminModel):
        user = User(**dict(request))
        user.id = old_user.id
        user.password = get_password_hash(request.password)
        user.updated_at = datetime.utcnow()
        return self.repository.update(user)

    def delete(self, user: User):
        return self.repository.delete(user)

    def check_username_email_exists(self, key: str, value: str):
        check_user = self.repository.find_element_by_key(key, value)
        if check_user:
            raise HTTPException(status_code=422, detail=f"Username or email already exists")
