from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db


router = APIRouter(
    prefix = "/exercises",
    tags = ["exercise_id"],
    responses = {404: {"desription": "Exercise not found"}},
)

@router.post("/", response_model = schemas.ExerciseRead, status_code = status.HTTP_201_CREATED)
def create_exercise(exercise_data: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    exercise = crud.create_exercise(db, exercise_data)
    if not exercise:
        raise HTTPException(status_code=400, detail="Workout not found")
    return exercise


@router.get("/{exercise_id}", response_model = schemas.ExerciseRead)
def read_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = crud.read_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code = 404, detail = "Exercise not found")
    return exercise


@router.get("/by-workout/{workout_id}", response_model = list[schemas.ExerciseRead])
def read_exercises_by_workout(workout_id: int, db: Session = Depends(get_db)):
    exercises = crud.read_exercises_by_workout(db, workout_id)
    if not exercises:
        return []
    return exercises


@router.delete("/{exercise_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    success = crud.delete_exercise(db, exercise_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "Exercise not found")
    return None


