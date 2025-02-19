from pydantic import BaseModel, constr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=15)

class UserCreate(UserBase):
    password: str = Field(min_length=6)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, value: str):
        if not re.match("^[a-zA-Z0-9_-]+$", value):
            raise ValueError("Username can only contain letters, numbers, underscores and hyphens")
        return value
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, value: str):
        # Check password strength
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search("[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search("[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search("[0-9]", value):
            raise ValueError("Password must contain at least one number")
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        
        # Check for common weak passwords
        common_passwords = ["Password123!", "Admin123!", "User123456!"]
        if value in common_passwords:
            raise ValueError("Password is too common, please use a more complex password")
            
        return value


class UserLogin(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True