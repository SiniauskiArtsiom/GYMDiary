from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

#--SET--

class SetBase(BaseModel):
    order: int
    weight: float
    reps: int

class SetCreate(SetBase):
    exercise_id: int

class SetUpdate(BaseModel):
    order: int | None = None
    weight: float | None = None
    reps: int | None = None

class SetRead(SetBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    exercise_id: int

#--EXERCISE--

class ExerciseBase(BaseModel):
    name: str
    order: int

class ExerciseCreate(ExerciseBase):
    workout_id: int

class ExerciseUpdate(BaseModel):
    name: str | None = None
    order: int | None = None

class ExerciseRead(ExerciseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    workout_id: int
    sets: list[SetRead] = Field(default_factory = list)

#--WORKOUT--

class WorkoutBase(BaseModel):
    started_at: datetime
    finished_at: datetime | None = None
    calories_burned: int | None = None

class WorkoutCreate(BaseModel):
    pass

class WorkoutFinish(BaseModel):
    calories_burned: int | None = None


class WorkoutRead(WorkoutBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    exercises: list[ExerciseRead] = Field(default_factory = list)

class WorkoutReadLightScheme(WorkoutBase):
    model_config = ConfigDict(from_attributes = True)
    id: int