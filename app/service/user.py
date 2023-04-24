from fastapi import Depends, Request
from datetime import datetime
from uuid import UUID

from models import UserModel, UserQueryRequest
from schemas import User, get_password_hash

from repositories import UserRepository
from .query_params import QueryParamsService


class UserService(QueryParamsService):
    repository: UserRepository

    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository = repository

    def list_by_request(self, company_id: UUID, request: Request):
        params = UserQueryRequest(**dict(request.query_params))
        params = self.transform_query_params(params)
        return self.repository.list(company_id, params)

    def list(self, company_id: UUID, params: dict):
        params = UserQueryRequest(**params)
        params = self.transform_query_params(params)
        return self.repository.list(company_id, params)

    def show(self, id: UUID):
        return self.repository.show(id)

    def create(self, company_id: UUID, request: UserModel):
        new_user = User(**dict(request))
        new_user.is_superadmin = False
        new_user.company_id = company_id
        new_user.password = get_password_hash(request.password)
        new_user.created_at = datetime.utcnow()
        return self.repository.create(new_user)

    def update(self, old_user: User, request: UserModel):
        user = User(**dict(request))
        user.id = old_user.id
        user.company_id = old_user.company_id
        user.password = get_password_hash(request.password)
        user.updated_at = datetime.utcnow()
        return self.repository.update(user)

    def delete(self, user: User):
        return self.repository.delete(user)

    def check_access_permission(self, user_company_id: UUID, admin_company_id: UUID):
        return str(user_company_id) == str(admin_company_id)
