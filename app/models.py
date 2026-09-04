from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)

    started_at = Column(DateTime, server_default=func.now(), nullable = False)
    finished_at = Column(DateTime, nullable = True)
    calories_burned = Column(Integer, nullable = True)

    exercises = relationship("Exercise", back_populates="workout", cascade = "all, delete-orphan")#,order_by = "Exercise.order")

class Exercise(Base):
    __tablename__ = "exercises"

    workout = relationship("Workout", back_populates="exercises")

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False, index = True)
    name = Column(String, nullable= False)
    order = Column(Integer, nullable = False)
    #time

    sets = relationship("Set", back_populates="exercise", cascade="all, delete-orphan")#,order_by = "Set.order")

class Set(Base):
    __tablename__ = "sets"

    exercise = relationship("Exercise", back_populates="sets")

    id = Column(Integer, primary_key = True, index = True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable = False, index = True)
    order = Column(Integer, nullable = False)
    reps = Column(Integer, nullable = False)
    weight = Column(Float, nullable = False)