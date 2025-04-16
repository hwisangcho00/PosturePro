from fastapi import FastAPI
from app.routers import users, workouts, metrics  # Import both users and workouts routers
from app.database import Base, engine

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to PosturePro API"}

# Include routers with consistent prefixes and tags
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])
