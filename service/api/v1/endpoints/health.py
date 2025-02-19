from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.health import UserHealthCreate, UserHealth, UserHealthUpdate
from crud import health as health_crud
from api.deps import get_db, get_current_user
from models.user import User

router = APIRouter()

@router.post("/health", response_model=UserHealth)
def create_user_health(
    health_info: UserHealthCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    health_info = health_crud.create_health_info(db, health_info, current_user.id)

    if not health_info:
        raise HTTPException(
            status_code=400,
            detail="Health information already exists."
        )
    return health_info

@router.get("/health", response_model=UserHealth)
def get_health_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    health_info = health_crud.get_health_info(db, user_id=current_user.id)
    if not health_info:
        raise HTTPException(status_code=404, detail="Health information not found")
    return health_info

@router.put("/health", response_model=UserHealth)
def update_user_health(
    health_update: UserHealthUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_health, error_msg = health_crud.update_health_info(
        db=db,
        user_id=current_user.id,
        health_update=health_update
    )
    
    if error_msg:
        raise HTTPException(
            status_code=404 if "not found" in error_msg else 400,
            detail=error_msg
        )
    
    return updated_health