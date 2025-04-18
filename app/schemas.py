from pydantic import BaseModel, UUID4, EmailStr
from datetime import datetime, timedelta
from typing import Optional, Any, Dict

class UserCreate(BaseModel):
    email: EmailStr
    password_hash: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

# Schema for WorkoutSession
class WorkoutSessionCreate(BaseModel):
    session_id: str
    email: EmailStr

class WorkoutSessionResponse(BaseModel):
    session_id: str
    email: EmailStr
    start_time: datetime
    end_time: Optional[datetime] = None

    # Declare `total_duration` as a property
    @property
    def total_duration(self) -> Optional[str]:
        # Convert timedelta to a string if it exists
        if hasattr(self, '_total_duration') and isinstance(self._total_duration, timedelta):
            return str(self._total_duration)
        return None

    @total_duration.setter
    def total_duration(self, value: Optional[timedelta]):
        self._total_duration = value

    class Config:
        from_attributes = True

# Schema for WorkoutSet
class WorkoutSetCreate(BaseModel):
    set_number: str
    session_id: str
    reps: Any
    weight: Optional[float] = None

class WorkoutSetResponse(BaseModel):
    set_number: str
    session_id: str
    weight: Optional[float]

    class Config:
        from_attributes = True

# Schema for WorkoutSet w/o reps
class WorkoutSetBasicCreate(BaseModel):
    set_number: str        # Provided by the mobile app
    session_id: str    # The associated workout session ID
    weight: Optional[float] = None

class WorkoutSetBasicResponse(BaseModel):
    set_id: str
    session_id: str
    weight: Optional[float]

    class Config:
        from_attributes = True

class WorkoutRepCreate(BaseModel):
    rep_number: str
    set_number: str
    session_id: str
    data: Any  # JSONB data

class WorkoutRepResponse(BaseModel):
    rep_id: str
    set_id: str
    data: Any  # JSONB data

    class Config:
        from_attributes = True  # Ensures SQLAlchemy objects can be converted to JSON

class FullWorkoutDataCreate(BaseModel):
    session_id: str
    email: EmailStr
    weight: Optional[float]
    set_number: str
    rep_number: str
    data: Any

class FullWorkoutDataResponse(BaseModel):

    rep_id: str
    set_id: str
    data: Any  # JSONB data

    class Config:
        from_attributes = True


class GoodRepCreate(BaseModel):
    data: Any


class BadRepCreate(BaseModel):
    data: Any


class GoodRepResponse(BaseModel):
    id: int
    data: Any

    class Config:
        from_attributes = True

class BadRepResponse(BaseModel):
    id: int
    data: Any

    class Config:
        from_attributes = True