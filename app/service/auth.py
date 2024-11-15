from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from starlette import status

from config import JWT_ALGORITHM, JWT_SECRET

from schemas import User, verify_password

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(user: User, expire_minutes: int = 5):
    expire_time = datetime.utcnow() + timedelta(minutes=expire_minutes)
    claims = {
        "sub": user.username,
        "id": str(user.id),
        "company_id": str(user.company_id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "is_superadmin": user.is_superadmin,
        "is_active": user.is_active,
        "exp": expire_time,
        'minutes': expire_minutes
    }
    return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token=token, key=JWT_SECRET,
                             algorithms=[JWT_ALGORITHM])
        if payload.get("id") is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Username or password is incorrect",
                                headers={"WWW-Authenticate": "Bearer"})
        user = User()
        user.username = payload.get("sub")
        user.id = payload.get("id")
        user.company_id = payload.get("company_id")
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.is_admin = payload.get("is_admin")
        user.is_active = payload.get("is_active")
        user.is_superadmin = payload.get("is_superadmin")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please login to continue",
                            headers={"WWW-Authenticate": "Bearer"})
