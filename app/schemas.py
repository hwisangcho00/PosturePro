from pydantic import BaseModel, UUID4
from datetime import datetime, timedelta
from typing import Optional, Any

class UserCreate(BaseModel):
    email: str
    password_hash: str
    first_name: str
    last_name: str

class UserResponse(BaseModel):
    user_id: UUID4
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        orm_mode = True  # Allows SQLAlchemy objects to be returned as Pydantic models

# Schema for WorkoutType
class WorkoutTypeBase(BaseModel):
    workout_type_id: str
    name: str
    description: Optional[str] = None

class WorkoutTypeResponse(WorkoutTypeBase):
    class Config:
        orm_mode = True

# Schema for WorkoutSession
class WorkoutSessionCreate(BaseModel):
    user_id: UUID4
    workout_type_id: str

class WorkoutSessionResponse(BaseModel):
    session_id: UUID4
    user_id: UUID4
    workout_type_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    created_at: datetime

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
        orm_mode = True

# Schema for WorkoutSet
class WorkoutSetCreate(BaseModel):
    session_id: UUID4
    set_number: int
    reps: int
    weight: Optional[float] = None

class WorkoutSetResponse(BaseModel):
    set_id: UUID4
    session_id: UUID4
    set_number: int
    reps: int
    weight: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True


class HardwareDataCreate(BaseModel):
    set_id: str
    data: Any

class HardwareDataResponse(BaseModel):
    set_id: str
    data: Any

    class Config:
        orm_mode = True