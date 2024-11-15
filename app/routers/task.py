from fastapi import APIRouter, Depends, Request, Query
from typing import List, Optional
from uuid import UUID

from models import BaseTaskViewModel, TaskViewModel, TaskModel
from schemas import User

from service import TaskService, token_interceptor

router = APIRouter(prefix="/tasks", tags=["Task"])


@router.get('', response_model=List[TaskViewModel])
async def get_tasks(
        paginate: int = Query(default=10),
        page: int = Query(default=1),
        sort: str = Query(default="id"),
        order: str = Query(default="asc"),
        search: str | None = None,
        admin: User = Depends(token_interceptor),
        service: TaskService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    params = {
        "paginate": paginate,
        "page": page,
        "sort": sort,
        "order": order,
        "search": search
    }
    return service.list(admin.company_id, params)


# Test by postman

@router.get('/request', response_model=List[TaskViewModel])
async def get_tasks_by_request(
        request: Request,
        admin: User = Depends(token_interceptor),
        service: TaskService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    return service.list_by_request(admin.company_id, request)


@router.get('/{task_id}', response_model=TaskViewModel)
async def get_task_by_id(
        task_id: UUID,
        admin: User = Depends(token_interceptor),
        service: TaskService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    task = service.show(task_id, admin.company_id)
    if not task:
        raise service.not_found_exception()
    return task


@router.post('', response_model=BaseTaskViewModel)
async def create_task(
        request: TaskModel,
        admin: User = Depends(token_interceptor),
        service: TaskService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    if not service.check_permission_to_create_task(admin.company_id, request.user_id):
        raise service.access_denied_exception()
    return service.create(request)


@router.put('/{task_id}', response_model=BaseTaskViewModel)
async def update_task(
        task_id: UUID,
        request: TaskModel,
        admin: User = Depends(token_interceptor),
        service: TaskService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    task = service.show(task_id, admin.company_id)
    if not task:
        raise service.not_found_exception()
    return service.update(task_id, request)


@router.delete('/{task_id}')
async def delete_task(
        task_id: UUID,
        admin: User = Depends(token_interceptor),
        service: TaskService = Depends()):
    if not service.check_admin_permission(admin):
        raise service.access_denied_exception()
    task = service.show(task_id, admin.company_id)
    if not task:
        raise service.not_found_exception()
    return service.delete(task)
