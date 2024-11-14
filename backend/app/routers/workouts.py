from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

# ----------- Workout Session -----------

# Endpoint to create a new workout session
@router.post("/workout_sessions/", response_model=schemas.WorkoutSessionResponse)
def create_workout_session(session: schemas.WorkoutSessionCreate, db: Session = Depends(get_db)):
    return crud.create_workout_session(db, session)

# Endpoint to get a workout session by session_id
@router.get("/workout_sessions/{session_id}", response_model=schemas.WorkoutSessionResponse)
def read_workout_session(session_id: str, db: Session = Depends(get_db)):
    db_session = crud.get_workout_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Workout session not found")
    return db_session

# Retrieve all workout sessions for a specific user
@router.get("/workout_sessions/user/{user_id}", response_model=list[schemas.WorkoutSessionResponse])
def get_sessions_by_user(user_id: str, db: Session = Depends(get_db)):
    sessions = crud.get_sessions_by_user_id(db, user_id=user_id)
    if not sessions:
        raise HTTPException(status_code=404, detail="No workout sessions found for this user")
    return sessions

# Retrieve all workout sessions of a specific workout type for a specific user
@router.get("/workout_sessions/type/{workout_type_id}/user/{user_id}", response_model=list[schemas.WorkoutSessionResponse])
def get_sessions_by_workout_type_and_user(workout_type_id: str, user_id: str, db: Session = Depends(get_db)):
    sessions = crud.get_sessions_by_workout_type_and_user(db, workout_type_id=workout_type_id, user_id=user_id)
    if not sessions:
        raise HTTPException(status_code=404, detail="No workout sessions found for this user and workout type")
    return sessions

# ----------- Workout Set -----------

# Endpoint to create a new workout set
@router.post("/workout_sets/", response_model=schemas.WorkoutSetResponse)
def create_workout_set(workout_set: schemas.WorkoutSetCreate, db: Session = Depends(get_db)):
    return crud.create_workout_set(db, workout_set)

# Endpoint to get a workout set by set_id
@router.get("/workout_sets/{set_id}", response_model=schemas.WorkoutSetResponse)
def read_workout_set(set_id: str, db: Session = Depends(get_db)):
    db_set = crud.get_workout_set(db, set_id=set_id)
    if db_set is None:
        raise HTTPException(status_code=404, detail="Workout set not found")
    return db_set

# Retrieve all sets for a specific workout session
@router.get("/workout_sets/session/{session_id}", response_model=list[schemas.WorkoutSetResponse])
def get_sets_by_session(session_id: str, db: Session = Depends(get_db)):
    sets = crud.get_sets_by_session_id(db, session_id=session_id)
    if not sets:
        raise HTTPException(status_code=404, detail="No workout sets found for this session")
    return sets