from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix = "/sets",
    tags = ["set_id"],
    responses = {404: {"description": "Set no found"}},
)


@router.post("/", response_model = schemas.SetRead, status_code = status.HTTP_201_CREATED)
def create_set(set_data: schemas.SetCreate, db: Session = Depends(get_db)):
    set = crud.create_set(db, set_data)
    if not set:
        raise HTTPException(status_code = 404, detail = "Exercise not found")
    return set


@router.get("/{set_id}", response_model = schemas.SetRead)
def read_set(set_id: int, db: Session = Depends(get_db)):
    set = crud.read_set(db, set_id)
    if not set:
        raise HTTPException(status_code = 404, detail = "Set not found")
    return set


@router.get("/by-exercise/{exercise_id}", response_model = list[schemas.SetRead])
def get_sets_by_exercise(exercise_id: int, db: Session = Depends(get_db)):
    sets = crud.read_sets_by_exercise(db, exercise_id)
    if not sets:
        return []
    return sets

@router.delete("/{set_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_set(set_id: int, db: Session = Depends(get_db)):
    success = crud.delete_set(db, set_id)
    if not success:
        raise HTTPException(status_code = 404, detail = "Set not found")
    return None

