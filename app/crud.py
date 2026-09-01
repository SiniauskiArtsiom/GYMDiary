from sqlalchemy.orm import Session, selectinload
from . import models, schemas
from datetime import datetime

#--CRUD Workout--

#--C--

def create_workout(db: Session) -> models.Workout:
    db_workout = models.Workout()
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def finish_workout(db: Session, workout_id: int, 
                  finish_data: schemas.WorkoutFinish) -> models.Workout:
    db_workout = db.get(models.Workout, workout_id)
    if not db_workout:
        return None
    db_workout.finished_at = datetime.now()
    if finish_data.calories_burned is not None:
        db_workout.calories_burned = finish_data.calories_burned
    db.commit()
    db.refresh(db_workout)
    return db_workout

#--R--

def read_workout(db: Session, workout_id: int) -> models.Workout:
    return (
        db.query(models.Workout)
        .options(
            selectinload(models.Workout.exercises).selectinload(models.Exercise.sets)
        )
        .filter(models.Workout.id == workout_id)
        .first()
    )

#--U--

def update_workout(db: Session, workout_id: int) -> models.Workout:
    pass


#--D--

def delete_workout(db: Session, workout_id: int) -> bool:
    db_workout = db.get(models.Workout, workout_id)
    if not db_workout:
        return False
    db.delete(db_workout)
    db.commit()
    return True


#--CRUD Exrcise--

#--C--

def create_exercise(db: Session, exercise_data: schemas.ExerciseCreate) -> models.Exercise:
    workout = db.get(models.Workout, exercise_data.workout_id)
    if not workout:
        return None

    db_exercise = models.Exercise(**exercise_data.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

#--R--

def read_exercise(db: Session, exercise_id: int) -> models.Exercise:
    return(
        db.query(models.Exercise)
        .options(
            selectinload(models.Exercise.sets)
        )
        .filter(models.Exercise.id == exercise_id)
        .first()
    )

def read_exercises_by_workout(db: Session, workout_id: int) -> list[models.Exercise]:
    return(
        db.query(models.Exercise)
        .options(
            selectinload(models.Exercise.sets)
        )
        .filter(models.Exercise.workout_id == workout_id)
        .order_by(models.Exercise.order)
        .all()
    )

#--U--

def update_exercise(db: Session, exercise_update: schemas.ExerciseUpdate) -> models.Exercise:
    pass

#--D--

def delete_exercise(db: Session, exercise_id: int) -> bool:
    db_exercise = db.get(models.Exercise, exercise_id)
    if not db_exercise:
        return False
    db.delete(db_exercise)
    db.commit()
    return True


#--CRUD Set--

#--C--

def create_set(db: Session, set_data: schemas.SetCreate) -> models.Set:
    exercise = db.get(models.Exercise, set_data.exercise_id)
    if not exercise:
        return None

    db_set = models.Set(**set_data.model_dump())
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

#--R--

def read_set(db: Session, set_id: int) -> models.Set:
    return db.get(models.Set, set_id)

def read_sets_by_exercise(db: Session, exercise_id: int) -> list[models.Set]:
    return(
        db.query(models.Set)
        .filter(models.Set.exercise_id == exercise_id)
        .order_by(models.Set.order)
        .all()
    )

#--U--

def update_set(db: Session, set_id: int, set_update: schemas.SetUpdate) -> models.Set:
    db_set = db.get(models.Set, set_id)
    if not db_set:
        return None
    update_data = set_update.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_set, key, value)
    db.commit()
    db.refresh(db_set)
    return(db_set)

#--D--

def delete_set(db: Session, set_id: int) -> bool:
    db_set = db.get(models.Set, set_id)
    if not db_set:
        return False
    db.delete(db_set)
    db.commit()
    return True