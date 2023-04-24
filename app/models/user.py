from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

from .request import BaseQueryRequest


class UserModel(BaseModel):
    email: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=255)
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    password: str = Field()
    is_active: Optional[bool] = Field(default=1)
    is_admin: Optional[bool] = Field(default=0)


class BaseUserViewModel(BaseModel):
    id: UUID
    company_id: UUID | None = None
    email: str
    username: str
    first_name: str
    last_name: str
    is_active: bool | None = None
    is_admin: bool | None = None

    class Config:
        orm_mode = True


class UserViewModel(BaseUserViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UserQueryRequest(BaseQueryRequest):
    is_admin: Optional[bool] = Field()

    def get_sort_fields(self):
        return ['id', 'first_name', 'username']

    def get_filter_fields(self):
        return ['is_admin']

    def get_search_fields(self):
        return ['username', 'first_name']
