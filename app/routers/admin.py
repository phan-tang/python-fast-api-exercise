from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from models import BaseUserViewModel, UserViewModel, AdminModel
from schemas import User

from service import AdminService, token_interceptor

router = APIRouter(prefix="/admins", tags=["Admin"])


@router.get('', response_model=List[UserViewModel])
async def get_admins(
        admin: User = Depends(token_interceptor),
        service: AdminService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    return service.list()


@router.get('/{admin_id}', response_model=UserViewModel)
async def get_admin_by_id(
        admin_id: UUID,
        admin: User = Depends(token_interceptor),
        service: AdminService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    user = service.show(admin_id)
    if not user:
        raise service.not_found_exception()
    return user


@router.post('', response_model=BaseUserViewModel)
async def create_admin(
        request: AdminModel,
        admin: User = Depends(token_interceptor),
        service: AdminService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    return service.create(request)


@router.put('/{admin_id}', response_model=BaseUserViewModel)
async def update_admin(
        user_id: UUID,
        request: AdminModel,
        admin: User = Depends(token_interceptor),
        service: AdminService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user:
        raise service.not_found_exception()
    return service.update(user, request)


@router.delete('/{admin_id}')
async def delete_admin(
        user_id: UUID,
        admin: User = Depends(token_interceptor),
        service: AdminService = Depends()):
    if not service.check_superadmin_permission(admin):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user:
        raise service.not_found_exception()
    return service.delete(user)
