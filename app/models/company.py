from pydantic import BaseModel, Field
from schemas import CompanyMode
from uuid import UUID
from datetime import datetime
from typing import Optional
from .request import BaseQueryRequest


class CompanyModel(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field()
    mode: CompanyMode = Field(default=CompanyMode.ACTIVE)
    rating: Optional[int] = Field(gt=0, lt=6, default=5)


class BaseCompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    mode: CompanyMode
    rating: int | None = None

    class Config:
        orm_mode = True


class CompanyViewModel(BaseCompanyViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class CompanyQueryRequest(BaseQueryRequest):
    rating: Optional[str] = Field()

    def get_sort_fields(self):
        return ['id', 'name', 'rating']

    def get_filter_fields(self):
        return ['rating']

    def get_search_fields(self):
        return ['name', 'description']
