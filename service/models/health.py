from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from database import Base
from schemas.health import DiabetesType, ActivityLevel

class UserHealth(Base):
    __tablename__ = "user_health"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    name = Column(String(50))
    gender = Column(String(10))
    height = Column(Integer)
    weight = Column(Integer)
    age = Column(Integer)
    activity_level = Column(Enum(ActivityLevel))
    diabetes_type = Column(Enum(DiabetesType))
    diagnosis_year = Column(Integer)
    complications = Column(String(200))
    treatment = Column(String(100))
    blood_sugar_status = Column(String(100))
    is_patient = Column(Boolean)