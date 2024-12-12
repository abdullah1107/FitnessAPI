from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal
from enum import Enum

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class GoalTypeEnum(str, Enum):
    Weight_Loss = "Weight Loss"
    Muscle_Gain = "Muscle Gain"
    Endurance = "Endurance"
    Flexibility = "Flexibility"

class MealTypeEnum(str, Enum):
    Breakfast = "Breakfast"
    Lunch = "Lunch"
    Dinner = "Dinner"
    Snack = "Snack"

#Users
class UserBase(BaseModel):
    FirstName: str
    LastName: str
    Email: str
    PasswordHash: str
    DateOfBirth: date
    Gender: str
    HeightCm: Decimal
    WeightKg: Decimal

class UserCreate(UserBase):
    pass

class User(UserBase):
    UserID: int

    class Config:
        orm_mode = True

#Workout
class WorkoutBase(BaseModel):
    WorkoutDate: date
    DurationMinutes: int
    CaloriesBurned: Decimal
    Notes: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    WorkoutID: int
    UserID: int

    class Config:
        orm_mode = True

#Exercise
class ExerciseBase(BaseModel):
    Name: str
    Sets: int
    Reps: int
    WeightKg: Decimal

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    ExerciseID: int
    WorkoutID: int

    class Config:
        orm_mode = True

# Nutrations
class NutritionBase(BaseModel):
    LogDate: date
    MealType: MealTypeEnum
    FoodItem: str
    Calories: Decimal
    ProteinG: Decimal
    CarbsG: Decimal
    FatG: Decimal

class NutritionCreate(NutritionBase):
    pass

class Nutrition(NutritionBase):
    NutritionID: int
    UserID: int

    class Config:
        orm_mode = True

# Goal
class GoalBase(BaseModel):
    GoalType: GoalTypeEnum
    TargetValue: Decimal
    CurrentValue: Decimal
    TargetDate: date

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    GoalID: int
    UserID: int

    class Config:
        orm_mode = True

######## Progress
class ProgressBase(BaseModel):
    weight_kg: float
    body_fat_percentage: float
    notes: Optional[str] = None

class ProgressCreate(ProgressBase):
    user_id: int
    log_date: date

class ProgressUpdate(BaseModel):
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    notes: Optional[str] = None
    log_date: Optional[date] = None

class Progress(ProgressBase):
    progress_id: int
    user_id: int
    log_date: date

    class Config:
        orm_mode = True



