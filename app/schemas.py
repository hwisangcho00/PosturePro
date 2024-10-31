from pydantic import BaseModel, UUID4
from datetime import datetime

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
