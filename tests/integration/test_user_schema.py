import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordUpdate
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

def valid_user_create_data():
    """Helper function to generate valid user creation data."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "username": "johndoe",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
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


def test_user_create_valid():
    """Test creating a valid UserCreate schema with all requirements met."""
    data = valid_user_create_data()
    user = UserCreate(**data)
    assert user.username == "johndoe"
    assert user.email == "john.doe@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.password == "SecurePass123!"
    assert user.confirm_password == "SecurePass123!"

def test_user_create_with_special_characters():
    """Test UserCreate with various special characters in password."""
    data = valid_user_create_data()
    data["password"] = "P@ssw0rd#2024!"
    data["confirm_password"] = "P@ssw0rd#2024!"
    user = UserCreate(**data)
    assert user.password == "P@ssw0rd#2024!"


def test_user_create_password_mismatch():
    """Test that UserCreate fails when passwords don't match."""
    data = valid_user_create_data()
    data["confirm_password"] = "DifferentPass123!"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "Passwords do not match" in str(exc_info.value)


def test_user_create_password_too_short():
    """Test that UserCreate fails when password is less than 8 characters."""
    data = valid_user_create_data()
    data["password"] = "Pass1!"
    data["confirm_password"] = "Pass1!"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    # Should fail at field validation level (min_length=8)
    assert "at least 8 characters" in str(exc_info.value).lower()


def test_user_create_password_no_uppercase():
    """Test that UserCreate fails when password has no uppercase letter."""
    data = valid_user_create_data()
    data["password"] = "securepass123!"
    data["confirm_password"] = "securepass123!"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "at least one uppercase letter" in str(exc_info.value)


def test_user_create_password_no_lowercase():
    """Test that UserCreate fails when password has no lowercase letter."""
    data = valid_user_create_data()
    data["password"] = "SECUREPASS123!"
    data["confirm_password"] = "SECUREPASS123!"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "at least one lowercase letter" in str(exc_info.value)

def test_user_create_password_no_digit():
    """Test that UserCreate fails when password has no digit."""
    data = valid_user_create_data()
    data["password"] = "SecurePass!"
    data["confirm_password"] = "SecurePass!"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "at least one digit" in str(exc_info.value)


def test_user_create_password_no_special_char():
    """Test that UserCreate fails when password has no special character."""
    data = valid_user_create_data()
    data["password"] = "SecurePass123"
    data["confirm_password"] = "SecurePass123"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "at least one special character" in str(exc_info.value)


def test_user_create_password_multiple_failures():
    """Test that UserCreate fails when password violates multiple requirements."""
    data = valid_user_create_data()
    data["password"] = "password"  # No uppercase, no digit, no special char
    data["confirm_password"] = "password"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    # Should fail on the first check (uppercase)
    error_str = str(exc_info.value)
    assert "uppercase" in error_str or "digit" in error_str or "special character" in error_str

def test_user_create_missing_username():
    """Test that UserCreate fails when username is missing."""
    data = valid_user_create_data()
    del data["username"]
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "required" in str(exc_info.value).lower()

def test_user_create_missing_email():
    """Test that UserCreate fails when email is missing."""
    data = valid_user_create_data()
    del data["email"]
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "required" in str(exc_info.value).lower()

def test_user_create_invalid_email():
    """Test that UserCreate fails when email format is invalid."""
    data = valid_user_create_data()
    data["email"] = "not-an-email"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "email" in str(exc_info.value).lower()


def test_user_create_username_too_short():
    """Test that UserCreate fails when username is less than 3 characters."""
    data = valid_user_create_data()
    data["username"] = "ab"
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "at least 3 characters" in str(exc_info.value).lower()

def test_user_create_username_too_long():
    """Test that UserCreate fails when username is more than 50 characters."""
    data = valid_user_create_data()
    data["username"] = "a" * 51
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(**data)
    assert "50" in str(exc_info.value) or "most" in str(exc_info.value).lower()


def test_password_update_valid():
    """Test creating a valid PasswordUpdate schema."""
    data = {
        "current_password": "OldPass123!",
        "new_password": "NewPass456!",
        "confirm_new_password": "NewPass456!"
    }
    pwd_update = PasswordUpdate(**data)
    assert pwd_update.current_password == "OldPass123!"
    assert pwd_update.new_password == "NewPass456!"

def test_password_update_mismatch():
    """Test that PasswordUpdate fails when new passwords don't match."""
    data = {
        "current_password": "OldPass123!",
        "new_password": "NewPass456!",
        "confirm_new_password": "DifferentPass!"
    }
    with pytest.raises(ValidationError) as exc_info:
        PasswordUpdate(**data)
    assert "do not match" in str(exc_info.value)

def test_password_update_same_as_current():
    """Test that PasswordUpdate fails when new password is same as current."""
    data = {
        "current_password": "SamePass123!",
        "new_password": "SamePass123!",
        "confirm_new_password": "SamePass123!"
    }
    with pytest.raises(ValidationError) as exc_info:
        PasswordUpdate(**data)
    assert "must be different" in str(exc_info.value)

def test_user_login_valid():
    """Test creating a valid UserLogin schema."""
    data = {
        "username": "johndoe",
        "password": "SecurePass123!"
    }
    login = UserLogin(**data)
    assert login.username == "johndoe"
    assert login.password == "SecurePass123!"

def test_user_login_missing_password():
    """Test that UserLogin fails when password is missing."""
    data = {
        "username": "johndoe"
    }
    with pytest.raises(ValidationError) as exc_info:
        UserLogin(**data)
    assert "required" in str(exc_info.value).lower()


def test_user_update_partial():
    """Test that UserUpdate allows partial updates."""
    data = {
        "first_name": "Jane"
    }
    update = UserUpdate(**data)
    assert update.first_name == "Jane"
    assert update.last_name is None
    assert update.email is None
    assert update.username is None

def test_user_update_all_fields():
    """Test that UserUpdate works with all fields."""
    data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "username": "janesmith"
    }
    update = UserUpdate(**data)
    assert update.first_name == "Jane"
    assert update.last_name == "Smith"
    assert update.email == "jane.smith@example.com"
    assert update.username == "janesmith"    

