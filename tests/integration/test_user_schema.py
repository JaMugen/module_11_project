import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.user import (
    UserLogin  ,
    UserResponse
)

def user_response_data():
    """Helper function to generate valid user response data."""
    return {
        "id": uuid4(),
        "username": "johndoe123",
        "email": "johndoe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_active": True,
        "is_verified": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

def test_user_response_valid():
    """Test creating a valid UserResponse schema."""
    data = user_response_data()
    user = UserResponse(**data)
    assert user.username == "johndoe123"
    assert user.email == "johndoe@example.com" 

def test_user_response_missing_email():
    """Test UserResponse fails if 'email' is missing."""
    data = user_response_data()
    del data["email"]
    with pytest.raises(ValidationError) as exc_info:
        UserResponse(**data)
    assert "required" in str(exc_info.value).lower()    