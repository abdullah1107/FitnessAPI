from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import Base, User, Workout, Exercise, Nutrition, Goal, Progress
from schemas import UserCreate, User, WorkoutCreate, Workout, ExerciseCreate, Exercise, NutritionCreate, Nutrition, GoalCreate, Goal, ProgressCreate, ProgressUpdate, Progress
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./Fitness.db"  # Use SQLite for simplicity

# Initialize FastAPI
app = FastAPI()

# SQLAlchemy Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User routes
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(FirstName=user.FirstName, LastName=user.LastName, Email=user.Email,
                   PasswordHash=user.PasswordHash, DateOfBirth=user.DateOfBirth,
                   Gender=user.Gender, HeightCm=user.HeightCm, WeightKg=user.WeightKg)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.UserID == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Workout routes
@app.post("/workouts/", response_model=Workout)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(UserID=workout.UserID, WorkoutDate=workout.WorkoutDate,
                         DurationMinutes=workout.DurationMinutes, CaloriesBurned=workout.CaloriesBurned,
                         Notes=workout.Notes)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.get("/workouts/{workout_id}", response_model=Workout)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    db_workout = db.query(Workout).filter(Workout.WorkoutID == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return db_workout

# Exercise routes
@app.post("/exercises/", response_model=Exercise)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = Exercise(WorkoutID=exercise.WorkoutID, Name=exercise.Name, Sets=exercise.Sets,
                           Reps=exercise.Reps, WeightKg=exercise.WeightKg)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@app.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    db_exercise = db.query(Exercise).filter(Exercise.ExerciseID == exercise_id).first()
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return db_exercise


#########################
@app.post("/nutrition/", response_model=Nutrition)
def create_nutrition(nutrition: NutritionCreate, db: Session = Depends(get_db)):
    db_nutrition = Nutrition(UserID=nutrition.UserID, LogDate=nutrition.LogDate, MealType=nutrition.MealType,
                             FoodItem=nutrition.FoodItem, Calories=nutrition.Calories,
                             ProteinG=nutrition.ProteinG, CarbsG=nutrition.CarbsG, FatG=nutrition.FatG)
    db.add(db_nutrition)
    db.commit()
    db.refresh(db_nutrition)
    return db_nutrition

@app.get("/nutrition/{nutrition_id}", response_model=Nutrition)
def get_nutrition(nutrition_id: int, db: Session = Depends(get_db)):
    db_nutrition = db.query(Nutrition).filter(Nutrition.NutritionID == nutrition_id).first()
    if db_nutrition is None:
        raise HTTPException(status_code=404, detail="Nutrition log not found")
    return db_nutrition

# Goal routes
@app.post("/goals/", response_model=Goal)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db)):
    db_goal = Goal(UserID=goal.UserID, GoalType=goal.GoalType, TargetValue=goal.TargetValue,
                   CurrentValue=goal.CurrentValue, TargetDate=goal.TargetDate)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@app.get("/goals/{goal_id}", response_model=Goal)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    db_goal = db.query(Goal).filter(Goal.GoalID == goal_id).first()
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal


#########################

# # Get all goals for a user
# @app.get("/goals/{user_id}", response_model=List[Goal])
# def get_goals(user_id: int, db: Session = Depends(get_db)):
#     db_goals = db.query(Goal).filter(Goal.user_id == user_id).all()
#     return db_goals

# # Update Goal endpoint
# @app.put("/goals/{goal_id}", response_model=Goal)
# def update_goal(goal_id: int, goal: GoalUpdate, db: Session = Depends(get_db)):
#     db_goal = db.query(Goal).filter(Goal.goal_id == goal_id).first()
#     if not db_goal:
#         raise HTTPException(status_code=404, detail="Goal not found")
    
#     if goal.current_value is not None:
#         db_goal.current_value = goal.current_value
#     if goal.target_date is not None:
#         db_goal.target_date = goal.target_date

#     db.commit()
#     db.refresh(db_goal)
#     return db_goal

# Create Progress entry endpoint
@app.post("/progress/", response_model=Progress)
def create_progress(progress: ProgressCreate, db: Session = Depends(get_db)):
    db_progress = Progress(user_id=progress.user_id, weight_kg=progress.weight_kg, 
                           body_fat_percentage=progress.body_fat_percentage, 
                           notes=progress.notes, log_date=progress.log_date)
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

# Get all progress entries for a user
@app.get("/progress/{user_id}", response_model=Progress)
def get_progress(user_id: int, db: Session = Depends(get_db)):
    db_progress = db.query(Progress).filter(Progress.user_id == user_id).all()
    return db_progress
