from sqlalchemy import  Column, String, DateTime, Integer, ForeignKey, DECIMAL, Interval
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB, UUID
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

class HardwareData(Base):
    __tablename__ = "hardware_data"

    set_id = Column(String, ForeignKey("workout_sets.set_id", ondelete="CASCADE"), primary_key=True)
    data = Column(JSONB, nullable=False)

class UserMetrics(Base):
    __tablename__ = "user_metrics"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Discuss at next meeting what to include in this user metrics 
    left_back = Column(DECIMAL(5, 2))
    right_back = Column(DECIMAL(5, 2))
    left_leg = Column(DECIMAL(5, 2))
    right_leg = Column(DECIMAL(5, 2))
    timestamp = Column(String, nullable=False)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "left_back": self.left_back,
            "right_back": self.right_back,
            "left_leg": self.left_leg,
            "right_leg": self.right_leg,
            "timestamp": self.timestamp
        }

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