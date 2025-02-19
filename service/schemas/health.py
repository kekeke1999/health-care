from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, field_validator
from enum import Enum

class DiabetesType(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"
    GESTATIONAL = "gestational"
    SPECIAL = "special"
    PRE = "pre"
    OTHER = "other"

class ActivityLevel(str, Enum):
    BEDRIDDEN = "bedridden"
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class UserHealthBase(BaseModel):
    name: str
    gender: Gender
    height: int
    weight: int
    age: int
    activity_level: ActivityLevel
    diabetes_type: DiabetesType
    diagnosis_year: int
    complications: str
    treatment: str
    blood_sugar_status: str
    is_patient: bool # True if the user is a patient, False if the user is a caregiver

    @field_validator('diagnosis_year')
    @classmethod
    def validate_diagnosis_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year:
                raise ValueError(f'Diagnosis year must be between 1900 and {current_year}')
        return v


class UserHealthCreate(UserHealthBase):
    pass

class UserHealth(UserHealthBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserHealthUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    age: Optional[int] = None
    activity_level: Optional[ActivityLevel] = None
    diabetes_type: Optional[DiabetesType] = None
    diagnosis_year: Optional[int] = None
    complications: Optional[str] = None
    treatment: Optional[str] = None
    blood_sugar_status: Optional[str] = None
    is_patient: Optional[bool] = None

    @field_validator('diagnosis_year')
    @classmethod
    def validate_diagnosis_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year:
                raise ValueError(f'Diagnosis year must be between 1900 and {current_year}')
        return v
