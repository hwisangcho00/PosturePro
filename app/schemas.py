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

# Schema for WorkoutType
class WorkoutTypeBase(BaseModel):
    workout_type_id: str
    name: str
    description: Optional[str] = None

class WorkoutTypeResponse(WorkoutTypeBase):
    class Config:
        from_attributes = True

# Schema for WorkoutSession
class WorkoutSessionCreate(BaseModel):
    session_id: str
    email: EmailStr
    workout_type_id: str

class WorkoutSessionResponse(BaseModel):
    session_id: str
    email: EmailStr
    workout_type_id: str
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
    session_id: str
    set_number: int
    reps: int
    weight: Optional[float] = None

class WorkoutSetResponse(BaseModel):
    set_id: str
    session_id: str
    set_number: int
    reps: int
    weight: Optional[float]

    class Config:
        from_attributes = True


class HardwareDataCreate(BaseModel):
    set_id: str
    data: Any

class HardwareDataResponse(BaseModel):
    set_id: str
    data: Any

    class Config:
        from_attributes = True