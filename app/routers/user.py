from fastapi import APIRouter, Depends, Request, Query
from uuid import UUID
from typing import List

from models import BaseUserViewModel, UserViewModel, UserModel
from schemas import User

from service import UserService, token_interceptor

router = APIRouter(prefix="/users", tags=["User"])


@router.get('', response_model=List[UserViewModel])
async def get_users(
        paginate: int = Query(default=10),
        page: int = Query(default=1),
        sort: str = Query(default="id"),
        order: str = Query(default="asc"),
        search: str | None = None,
        is_admin: bool | None = None,
        admin: User = Depends(token_interceptor),
        service: UserService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    params = {
        "paginate": paginate,
        "page": page,
        "sort": sort,
        "order": order,
        "search": search,
        "is_admin": is_admin
    }
    return service.list(admin.company_id, params)


# Test by postman

@router.get('/request', response_model=List[UserViewModel])
async def get_users_by_request(
        request: Request,
        admin: User = Depends(token_interceptor),
        service: UserService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    return service.list_by_request(admin.company_id, request)


@router.get('/{user_id}', response_model=UserViewModel)
async def get_user_by_id(
        user_id: UUID,
        admin: User = Depends(token_interceptor),
        service: UserService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user or not service.check_access_permission(user.company_id, admin.company_id):
        raise service.not_found_exception()
    return user


@router.post('', response_model=BaseUserViewModel)
async def create_user(
        request: UserModel,
        admin: User = Depends(token_interceptor),
        service: UserService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    return service.create(admin.company_id, request)


@router.put('/{user_id}', response_model=BaseUserViewModel)
async def update_user(
        user_id: UUID,
        request: UserModel,
        admin: User = Depends(token_interceptor),
        service: UserService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user or not service.check_access_permission(user.company_id, admin.company_id):
        raise service.not_found_exception()
    return service.update(user, request)


@router.delete('/{user_id}')
async def delete_user(
        user_id: UUID,
        admin: User = Depends(token_interceptor),
        service: UserService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user or not service.check_access_permission(user.company_id, admin.company_id):
        raise service.not_found_exception()
    return service.delete(user)
