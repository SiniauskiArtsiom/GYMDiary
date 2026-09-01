from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix = "/workouts",
    tags = ["workouts"],
    responses = {404: {"description": "Workout not found"}},
)


@router.post("/", response_model = schemas.WorkoutRead, status_code = status.HTTP_201_CREATED)
def create_workout(db: Session = Depends(get_db)):
    workout = crud.create_workout(db)
    return workout


@router.post("/{workout_id}/finish", response_model = schemas.WorkoutRead)
def finish_workout(workout_id: int, finish_data: schemas.WorkoutFinish, db: Session = Depends(get_db)):
    workout = crud.finish_workout(db, workout_id, finish_data)
    if not workout:
        raise HTTPException(status_code = 404, detail = "Workout not found")
    return workout

@router.get("/{workout_id}", response_model = schemas.WorkoutRead)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = crud.read_workout(db, workout_id)
    if not workout:
        raise HTTPException(status_code = 404, detail = "Workout not found")
    return workout

@router.delete("/{workout_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    success = crud.delete_workout(db, workout_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "Workout not found")
    return None