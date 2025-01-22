from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional

# ----------- User CRUD Operations -----------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        password_hash=user.password_hash,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

# ----------- Workout Type CRUD Operations -----------

def get_workout_type(db: Session, workout_type_id: str):
    return db.query(models.WorkoutType).filter(models.WorkoutType.workout_type_id == workout_type_id).first()

# ----------- Workout Session CRUD Operations -----------

def create_workout_session(db: Session, session: schemas.WorkoutSessionCreate):
    db_session = models.WorkoutSession(
        user_id=session.user_id,
        workout_type_id=session.workout_type_id,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_workout_session(db: Session, session_id: str):
    return db.query(models.WorkoutSession).filter(models.WorkoutSession.session_id == session_id).first()

def get_sessions_by_user_id(db: Session, user_id: str):
    return db.query(models.WorkoutSession).filter(models.WorkoutSession.user_id == user_id).all()

def get_sessions_by_workout_type_and_user(db: Session, workout_type_id: str, user_id: str):
    return db.query(models.WorkoutSession).filter(
        models.WorkoutSession.workout_type_id == workout_type_id,
        models.WorkoutSession.user_id == user_id
    ).all()

# ----------- Workout Set CRUD Operations -----------

def create_workout_set(db: Session, workout_set: schemas.WorkoutSetCreate):
    db_set = models.WorkoutSet(
        session_id=workout_set.session_id,
        set_number=workout_set.set_number,
        reps=workout_set.reps,
        weight=workout_set.weight,
    )
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

def get_workout_set(db: Session, set_id: str):
    return db.query(models.WorkoutSet).filter(models.WorkoutSet.set_id == set_id).first()

# Retrieve all sets for a specific workout session
def get_sets_by_session_id(db: Session, session_id: str):
    return db.query(models.WorkoutSet).filter(models.WorkoutSet.session_id == session_id).all()

# ----------- Hardware Data CRUD Operations -----------
def create_hardware_data(db: Session, hardware_data: schemas.HardwareDataCreate):
    db_data = models.HardwareData(
        set_id=hardware_data.set_id,
        data=hardware_data.data
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_average_by_set_id(db: Session, set_id: str) -> Optional[dict]:
    # Query the database for the hardware data
    hardware_data = db.query(models.HardwareData).filter(models.HardwareData.set_id == set_id).first()

    if not hardware_data:
        return None

    # Parse the JSON data
    data = hardware_data.data

    # Ensure the required keys exist
    required_keys = ['xs', 'ys', 'zs', 'gxs', 'gys', 'gzs', 'envs', 'raws', 'rects']
    if not all(key in data for key in required_keys):
        raise ValueError("Missing required keys in hardware data JSON")

    # Compute the averages for each array
    averages = {key: sum(data[key]) / len(data[key]) if data[key] else 0 for key in required_keys}

    # Return the analysis result
    return {
        "set_id": hardware_data.set_id,
        "averages": averages
    }