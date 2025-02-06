from sqlalchemy import  Column, String, DateTime, Integer, ForeignKey, DECIMAL, Interval
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB, UUID
import uuid

class User(Base):
    __tablename__ = "users"

    email = Column(String(255), primary_key=True, unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))

# class HardwareData(Base):
#     __tablename__ = "hardware_data"

#     set_id = Column(String(255), primary_key=True)
#     data = Column(JSONB, nullable=False)

# class UserMetrics(Base):
#     __tablename__ = "user_metrics"

#     user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     # Discuss at next meeting what to include in this user metrics 
#     left_back = Column(DECIMAL(5, 2))
#     right_back = Column(DECIMAL(5, 2))
#     left_leg = Column(DECIMAL(5, 2))
#     right_leg = Column(DECIMAL(5, 2))
#     timestamp = Column(String, nullable=False)

#     def to_dict(self):
#         return {
#             "user_id": self.user_id,
#             "left_back": self.left_back,
#             "right_back": self.right_back,
#             "left_leg": self.left_leg,
#             "right_leg": self.right_leg,
#             "timestamp": self.timestamp
#         }

class WorkoutType(Base):
    __tablename__ = "workout_types"

    workout_type_id = Column(String(50), primary_key=True)  # e.g., "squat", "deadlift"
    name = Column(String(100), nullable=False)
    description = Column(String)

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    session_id = Column(String(100), primary_key=True)
    email = Column(String(255), ForeignKey("users.email", ondelete="CASCADE"), nullable=False)
    workout_type_id = Column(String(50), ForeignKey("workout_types.workout_type_id", ondelete="SET NULL"))
    start_time = Column(DateTime, default=datetime.now(timezone.utc))
    end_time = Column(DateTime)
    total_duration = Column(Interval)

    user = relationship("User")
    workout_type = relationship("WorkoutType")

class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    set_id = Column(String(150), primary_key=True)  # session_id + _setNumber
    session_id = Column(String(100), ForeignKey("workout_sessions.session_id", ondelete="CASCADE"), nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(DECIMAL(5,2), nullable=True)

class WorkoutRep(Base):
    __tablename__ = "workout_reps"

    rep_id = Column(String(150), primary_key=True)  # set_id + _repNumber
    set_id = Column(String(150), ForeignKey("workout_sets.set_id", ondelete="CASCADE"), nullable=False)
    data = Column(JSONB, nullable=False)