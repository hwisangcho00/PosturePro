from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from typing import List

router = APIRouter()

# ----------- Workout Session -----------

@router.post("/sessions", response_model=schemas.WorkoutSessionResponse)
def add_workout_session(session_data: schemas.WorkoutSessionCreate, db: Session = Depends(get_db)):
    """API endpoint to create a new workout session."""
    return crud.create_workout_session(db, session_data)

@router.get("/sessions/{email}", response_model=List[schemas.WorkoutSessionResponse])
def get_workout_sessions(
    email: str,
    limit: int = Query(10, ge=1, le=50),  # Default = 5, min = 1, max = 50
    db: Session = Depends(get_db)
):
    """API endpoint to get latest workout sessions for a user, with adjustable limit."""
    return crud.get_workout_sessions_by_email(db, email, limit)


# ----------- Workout Set -----------

# Endpoint to create a new workout set
@router.post("/sets/", response_model=schemas.WorkoutSetResponse)
def create_workout_set(workout_set: schemas.WorkoutSetCreate, db: Session = Depends(get_db)):
    return crud.create_workout_set(db, workout_set)

# Endpoint to get a workout set by set_id
@router.get("/sets/{set_id}", response_model=schemas.WorkoutSetResponse)
def read_workout_set(set_id: str, db: Session = Depends(get_db)):
    db_set = crud.get_workout_set(db, set_id=set_id)
    if db_set is None:
        raise HTTPException(status_code=404, detail="Workout set not found")
    return db_set

# Retrieve all sets for a specific workout session
@router.get("/sets/session/{session_id}", response_model=list[schemas.WorkoutSetResponse])
def get_sets_by_session(session_id: str, db: Session = Depends(get_db)):
    sets = crud.get_sets_by_session_id(db, session_id=session_id)
    if not sets:
        raise HTTPException(status_code=404, detail="No workout sets found for this session")
    return sets