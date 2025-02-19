from sqlalchemy.orm import Session
from models.health import UserHealth
from schemas.health import UserHealthCreate, UserHealthUpdate
from typing import Optional, Tuple

def create_health_info(db: Session, health_info: UserHealthCreate, user_id: int):
    existing_health = db.query(UserHealth).filter(UserHealth.user_id == user_id).first()
    
    if existing_health:
        return None
    
    db_health = UserHealth(**health_info.dict(), user_id=user_id)
    db.add(db_health)
    db.commit()
    db.refresh(db_health)
    return db_health

def get_health_info(db: Session, user_id: int):
    return db.query(UserHealth).filter(UserHealth.user_id == user_id).first()

def update_health_info(
    db: Session,
    user_id: int,
    health_update: UserHealthUpdate
) -> Tuple[Optional[UserHealth], Optional[str]]:
    try:
        # First find the health info
        health_info = db.query(UserHealth).filter(
            UserHealth.user_id == user_id
        ).first()

        if not health_info:
            return None, "Health information not found"

        # Update only provided fields
        update_data = health_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(health_info, field, value)

        try:
            db.commit()
            db.refresh(health_info)
            return health_info, None
        except Exception as e:
            db.rollback()
            return None, f"Database error: {str(e)}"

    except Exception as e:
        return None, f"Error updating health information: {str(e)}"