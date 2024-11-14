from sqlalchemy import  Column, String, DateTime, Integer, ForeignKey, DECIMAL, Interval
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
import uuid

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_login = Column(DateTime)

class WorkoutType(Base):
    __tablename__ = "workout_types"

    workout_type_id = Column(String(50), primary_key=True)  # e.g., "squat", "deadlift"
    name = Column(String(100), nullable=False)
    description = Column(String)

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    workout_type_id = Column(String(50), ForeignKey("workout_types.workout_type_id", ondelete="SET NULL"))
    start_time = Column(DateTime, default=datetime.now(timezone.utc))
    end_time = Column(DateTime)
    total_duration = Column(Interval)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User")
    workout_type = relationship("WorkoutType")

class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    set_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("workout_sessions.session_id", ondelete="CASCADE"))
    set_number = Column(Integer)
    reps = Column(Integer)
    weight = Column(DECIMAL(5, 2))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    session = relationship("WorkoutSession")