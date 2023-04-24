from fastapi import Depends, Request
from datetime import datetime
from uuid import UUID

from schemas import Company
from models import CompanyQueryRequest, CompanyModel

from repositories import CompanyRepository
from .query_params import QueryParamsService


class CompanyService(QueryParamsService):
    repository: CompanyRepository

    def __init__(self, repository: CompanyRepository = Depends()) -> None:
        self.repository = repository

    def list_by_request(self, request: Request):
        params = CompanyQueryRequest(**dict(request.query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def list(self, params: dict):
        params = CompanyQueryRequest(**params)
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def show(self, id: UUID):
        return self.repository.show(id)

    def create(self, request: CompanyModel):
        company = Company(**dict(request))
        company.created_at = datetime.utcnow()
        return self.repository.create(company)

    def update(self, company_id: UUID, request: CompanyModel):
        company = Company(**dict(request))
        company.id = company_id
        company.updated_at = datetime.utcnow()
        return self.repository.update(company)

    def delete(self, company: Company):
        return self.repository.delete(company)
