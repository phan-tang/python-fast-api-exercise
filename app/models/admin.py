from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class AdminModel(BaseModel):
    company_id: UUID = Field()
    email: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=255)
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    password: str = Field()
    is_active: Optional[bool] = Field(default=1)
