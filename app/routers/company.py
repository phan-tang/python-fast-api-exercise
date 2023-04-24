from fastapi import APIRouter, Depends, Request
from starlette import status
from uuid import UUID
from typing import List

from models import BaseCompanyViewModel, CompanyViewModel, CompanyModel
from schemas import User
from service import CompanyService, token_interceptor

router = APIRouter(prefix='/companies', tags=["Company"])


@router.get('', response_model=List[CompanyViewModel])
async def get_companies(request: Request, service: CompanyService = Depends()):
    return service.list(request)


@router.get('/{company_id}', response_model=CompanyViewModel)
async def get_company_by_id(
        company_id: UUID,
        service: CompanyService = Depends()):
    company = service.show(company_id)
    return company


@router.post('', status_code=status.HTTP_201_CREATED, response_model=BaseCompanyViewModel)
async def create_company(
        request: CompanyModel,
        admin: User = Depends(token_interceptor),
        service: CompanyService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    return service.create(request)


@router.put('/{company_id}', response_model=BaseCompanyViewModel)
async def update_company(
        company_id: UUID,
        request: CompanyModel,
        admin: User = Depends(token_interceptor),
        service: CompanyService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    company = service.show(company_id)
    if not company or str(company_id) != str(admin.company_id):
        raise service.not_found_exception()
    return service.update(company_id, request)


@router.delete('/{company_id}')
async def delete_company(
        company_id: UUID,
        admin: User = Depends(token_interceptor),
        service: CompanyService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    company = service.show(company_id)
    if not company:
        raise service.not_found_exception()
    return service.delete(company)
