from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from database import get_db_session
from service import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    user = auth_service.authenticate_user(
        form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot find this user")
    token = auth_service.create_access_token(user, 30)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
