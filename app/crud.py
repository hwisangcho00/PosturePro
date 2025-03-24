import random
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List
from sqlalchemy.dialects.postgresql import insert
import json
from datetime import datetime, timedelta


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
        email=session_data.email
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

def generate_set_id(session_id, set_number):
    return f"{session_id}_{set_number}"

def generate_rep_id(session_id, set_number, rep_number):
    return f"{session_id}_{set_number}_{rep_number}"

# ----------- Workout Set CRUD Operations -----------

def create_basic_workout_set(db: Session, set_data: schemas.WorkoutSetBasicCreate):
    db_set = models.WorkoutSet(
        set_id= generate_set_id(set_data.session_id, set_data.set_number),
        session_id=set_data.session_id,
        weight=set_data.weight
    )
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

def create_workout_set(db: Session, set_data: schemas.WorkoutSetCreate):
    try:
        # Step 1: Create and commit the workout set first
        db_set = models.WorkoutSet(
            set_id= generate_set_id(set_data.session_id, set_data.set_number),
            session_id=set_data.session_id,
            weight=set_data.weight
        )
        db.add(db_set)
        db.commit()  # Commit the set first to ensure FK integrity
        db.refresh(db_set)

        # Step 2: Parse JSON reps data correctly
        parsed_reps = json.loads(set_data.reps) if isinstance(set_data.reps, str) else set_data.reps
        if not isinstance(parsed_reps, dict):
            raise ValueError("Invalid format for reps data. Expected a dictionary.")

        # Step 3: Add each rep to the workout_reps table
        for rep_number, rep_data in parsed_reps.items():
            set_id = generate_set_id(set_data.session_id, set_data.set_number)
            rep_id = generate_rep_id(set_data.session_id, set_data.set_number, rep_number)  # Generate unique rep_id
            
            db_rep = models.WorkoutRep(rep_id=rep_id, set_id=set_id, data=rep_data)
            db.add(db_rep)

        db.commit()  # Commit all reps at once
        return db_set

    except Exception as e:
        db.rollback()  # Rollback transaction in case of an error
        raise e  # Raise the error for debugging/logging


def get_workout_set(db: Session, set_id: str):
    return db.query(models.WorkoutSet).filter(models.WorkoutSet.set_id == set_id).first()

# Retrieve all sets for a specific workout session
def get_sets_by_session_id(db: Session, session_id: str):
    return db.query(models.WorkoutSet).filter(models.WorkoutSet.session_id == session_id).all()


# ----------- Workout Rep CRUD Operations -----------
def create_workout_rep(db: Session, rep_data: schemas.WorkoutRepCreate):

    rep_id = generate_rep_id(rep_data.session_id, rep_data.set_number, rep_data.rep_number)
    set_id = generate_set_id(rep_data.session_id, rep_data.set_number)

    db_rep = models.WorkoutRep(
        rep_id=rep_id,
        set_id=set_id,
        data=rep_data.data
    )
    db.add(db_rep)
    db.commit()
    db.refresh(db_rep)
    return db_rep

def get_rep_data_by_rep_id(db: Session, rep_id: str):
    return db.query(models.WorkoutRep).filter(models.WorkoutRep.rep_id == rep_id).first()


# ----------- Full Workout CRUD Operations -----------

def create_full_workout_data(db: Session, full_data: schemas.FullWorkoutDataCreate):

    set_id = generate_set_id(full_data.session_id, full_data.set_number)
    rep_id = generate_rep_id(full_data.session_id, full_data.set_number, full_data.rep_number)

    # 1. Check for the session
    session = db.query(models.WorkoutSession).filter(
        models.WorkoutSession.session_id == full_data.session_id
    ).first()
    if not session:
        session = models.WorkoutSession(
            session_id=full_data.session_id,
            email=full_data.email,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # 2. Check for the set
    workout_set = db.query(models.WorkoutSet).filter(
        models.WorkoutSet.set_id == set_id
    ).first()
    if not workout_set:
        workout_set = models.WorkoutSet(
            set_id=set_id,
            session_id=full_data.session_id,
            weight=full_data.weight,
        )
        db.add(workout_set)
        db.commit()
        db.refresh(workout_set)
    
    # 3. Create or update the rep
    rep = db.query(models.WorkoutRep).filter(
        models.WorkoutRep.rep_id == rep_id
    ).first()
    if not rep:
        rep = models.WorkoutRep(
            rep_id=rep_id,
            set_id=set_id,
            data=full_data.data
        )
        db.add(rep)
        db.commit()
        db.refresh(rep)
    else:
        rep.data = full_data.data
        db.commit()
        db.refresh(rep)
    
    return rep


# --------------- Form Data CRUD Operations ---------------

def get_form_status_by_rep_id(db: Session, rep_id: str):
    return random.choice([True, False])  



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

