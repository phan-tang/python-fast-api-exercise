from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, ForeignKey, Uuid, DateTime
from database import Base
from .base_entity import BaseEntity
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base, BaseEntity):
    __tablename__ = 'users'

    company_id = Column(Uuid, ForeignKey('companies.id'), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=1)
    is_admin = Column(Boolean, default=0)
    is_superadmin = Column(Boolean, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    company = relationship('Company')


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)
