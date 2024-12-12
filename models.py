from sqlalchemy import Column, Integer, String, Date,Text, ForeignKey, Enum, TIMESTAMP, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class GoalTypeEnum(enum.Enum):
    Weight_Loss = "Weight Loss"
    Muscle_Gain = "Muscle Gain"
    Endurance = "Endurance"
    Flexibility = "Flexibility"

class MealTypeEnum(enum.Enum):
    Breakfast = "Breakfast"
    Lunch = "Lunch"
    Dinner = "Dinner"
    Snack = "Snack"

class User(Base):
    __tablename__ = "users"
    
    UserID = Column(Integer, primary_key=True, index=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Email = Column(String(100), unique=True, index=True)
    PasswordHash = Column(String(255))
    DateOfBirth = Column(Date)
    Gender = Column(Enum(GenderEnum))
    HeightCm = Column(DECIMAL(5, 2))
    WeightKg = Column(DECIMAL(5, 2))
    CreatedAt = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    workouts = relationship("Workout", back_populates="user")
    nutrition_logs = relationship("Nutrition", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    progress = relationship("Progress", back_populates="progress")

class Workout(Base):
    __tablename__ = "workouts"
    
    WorkoutID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))
    WorkoutDate = Column(Date)
    DurationMinutes = Column(Integer)
    CaloriesBurned = Column(DECIMAL(5, 2))
    Notes = Column(Text)

    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")

class Exercise(Base):
    __tablename__ = "exercises"
    
    ExerciseID = Column(Integer, primary_key=True, index=True)
    WorkoutID = Column(Integer, ForeignKey('workouts.WorkoutID'))
    Name = Column(String(100))
    Sets = Column(Integer)
    Reps = Column(Integer)
    WeightKg = Column(DECIMAL(5, 2))

    workout = relationship("Workout", back_populates="exercises")

class Nutrition(Base):
    __tablename__ = "nutrition"
    NutritionID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))
    LogDate = Column(Date)
    MealType = Column(Enum(MealTypeEnum))
    FoodItem = Column(String(100))
    Calories = Column(DECIMAL(5, 2))
    ProteinG = Column(DECIMAL(5, 2))
    CarbsG = Column(DECIMAL(5, 2))
    FatG = Column(DECIMAL(5, 2))

    user = relationship("User", back_populates="nutrition_logs")

class Goal(Base):
    __tablename__ = "goals"
    GoalID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, ForeignKey('users.UserID'))
    GoalType = Column(Enum(GoalTypeEnum))
    TargetValue = Column(DECIMAL(5, 2))
    CurrentValue = Column(DECIMAL(5, 2))
    TargetDate = Column(Date)

    user = relationship("User", back_populates="goals")

class Progress(Base):
    __tablename__ = "progress"
    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.UserID"))
    log_date = Column(Date)
    weight_kg = Column(Float)
    body_fat_percentage = Column(Float)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="progress")

# class Admin(Base):
#     __tablename__ = "admins"
    
#     AdminID = Column(Integer, primary_key=True, index=True)
#     Username = Column(String(50), unique=True)
#     PasswordHash = Column(String(255))
#     CreatedAt = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')


   


