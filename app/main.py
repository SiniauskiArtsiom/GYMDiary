from fastapi import FastAPI
from .database import Base, engine
from . import models  
from .routers import workouts, exercises, sets

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "GYMDiary")

app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(sets.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}