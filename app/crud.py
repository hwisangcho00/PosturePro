from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List
from sqlalchemy.dialects.postgresql import insert


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

# ----------- Workout Type CRUD Operations -----------

def get_workout_type(db: Session, workout_type_id: str):
    return db.query(models.WorkoutType).filter(models.WorkoutType.workout_type_id == workout_type_id).first()

# ----------- Workout Session CRUD Operations -----------


def create_workout_session(db: Session, session_data: schemas.WorkoutSessionCreate):
    """Create a new workout session with email + timestamp as session_id."""
    db_session = models.WorkoutSession(
        session_id=session_data.session_id,
        email=session_data.email,
        workout_type_id=session_data.workout_type_id,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_workout_sessions_by_email(db: Session, email: str, limit: int = 10) -> List[schemas.WorkoutSessionResponse]:
    """Retrieve latest workout sessions for a given user email."""
    sessions = (
        db.query(models.WorkoutSession)
        .filter(models.WorkoutSession.email == email)
        .order_by(models.WorkoutSession.session_id.desc())  # Sort newest first
        .limit(limit)
        .all()
    )
    return sessions

# ----------- Workout Set CRUD Operations -----------

def generate_set_id(session_id: str, set_number: int) -> str:
    """Generate a unique set_id using session_id + _setNumber."""
    return f"{session_id}_{set_number}"

def create_workout_set(db: Session, set_data: schemas.WorkoutSetCreate):
    """Create a new workout set with a structured set_id."""
    set_id = generate_set_id(set_data.session_id, set_data.set_number)

    db_set = models.WorkoutSet(
        set_id=set_id,
        session_id=set_data.session_id,
        set_number=set_data.set_number,
        reps=set_data.reps,
        weight=set_data.weight
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
    stmt = insert(models.HardwareData).values(
        set_id=hardware_data.set_id,
        data=hardware_data.data
    ).on_conflict_do_update(
        index_elements=["set_id"],  # Primary key (ensures unique constraint)
        set_={"data": hardware_data.data}  # Update the data field if `set_id` exists
    )

    db.execute(stmt)
    db.commit()

    # Retrieve and return the updated row
    return db.query(models.HardwareData).filter(models.HardwareData.set_id == hardware_data.set_id).first()

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
        "data": averages
    }

