from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.security import get_password_hash
from datetime import datetime, timedelta
from typing import Union

def check_username_availability(db: Session, username: str) -> bool:
    existing_user = db.query(User).filter(User.username == username).first()
    return existing_user is None

def validate_password_not_similar_to_username(username: str, password: str) -> bool:
    username_lower = username.lower()
    password_lower = password.lower()
    
    # Check if password contains username
    if username_lower in password_lower or password_lower in username_lower:
        return False
    
    return True


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_create: UserCreate) -> tuple[bool, str, Union[User, None]]:
    try:
        # Check if username already exists
        if not check_username_availability(db, user_create.username):
            return False, "Username is already taken", None

        # Check if password is too similar to username
        if not validate_password_not_similar_to_username(user_create.username, user_create.password):
            return False, "Password cannot contain username", None

        # Create new user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            username=user_create.username,
            hashed_password=hashed_password,
            failed_attempts=0
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return True, "", db_user
        
    except Exception as e:
        db.rollback()
        return False, f"Registration failed: {str(e)}", None

def update_login_attempts(db: Session, user: User, failed: bool):
    if failed:
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(hours=1)
    else:
        user.failed_attempts = 0
        user.locked_until = None
    db.commit()