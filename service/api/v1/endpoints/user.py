from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from grpc import Status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin
from crud import user as user_crud
from core.security import verify_password, create_access_token
from config import settings
from api.deps import get_db
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.post("/register", response_model=Dict[str, Any])
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    success, error_message, user = user_crud.create_user(db, user_create)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail={
                "message": error_message,
                "error": True,
                "redirect_url": "/register" 
            }
        )
    
    return {
        "message": "Registration successful",
        "username": user.username,
        "redirect_url": "/login"  # Frontend can use this URL for redirection
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if db_user.locked_until and db_user.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Account is locked. Please try again later")
    
    if not verify_password(user.password, db_user.hashed_password):
        user_crud.update_login_attempts(db, db_user, failed=True)
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user_crud.update_login_attempts(db, db_user, failed=False)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
