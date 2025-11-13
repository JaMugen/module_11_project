from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserResponse(BaseModel):
    """Schema for user response data"""
    id: UUID
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Enable mapping from ORM objects


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe123",
                "password": "SecurePass123",
            }
        }
    )