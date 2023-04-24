from fastapi import HTTPException
from starlette import status

from schemas import User


class BaseService:

    def check_superadmin_permission(self, user: User):
        return (user.is_superadmin and user.is_active)

    def check_admin_permission(self, user: User):
        return (user.is_admin and user.is_active)

    def access_denied_exception(self, detail="Access denied"):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail)

    def not_found_exception(self, detail="This item doesn't exist"):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail)

    def token_exception(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"})
