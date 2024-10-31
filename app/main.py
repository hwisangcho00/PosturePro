from fastapi import FastAPI
from app.routers import users
from app.database import Base, engine

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Include routers
app.include_router(users.router)
