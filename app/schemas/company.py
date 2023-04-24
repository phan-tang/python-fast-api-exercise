import enum
from sqlalchemy import Column, String, Enum, Numeric, DateTime
from database import Base
from .base_entity import BaseEntity


class CompanyMode(enum.Enum):
    ACTIVE = 'A'
    INACTIVE = 'I'


class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String(255), nullable=False)
    description = Column(String)
    mode = Column(Enum(CompanyMode), nullable=False,
                  default=CompanyMode.ACTIVE)
    rating = Column(Numeric)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
