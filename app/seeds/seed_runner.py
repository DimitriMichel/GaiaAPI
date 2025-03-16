# app/seeds/seed_runner.py
import os
import sys
from sqlalchemy.orm import Session
import random

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import (
    User, Profile, DailyLog, FoodEntry, ExerciseEntry, 
    WorkEntry, EventEntry, MoodEntry, ActivityRecommendation, 
    MealType, IntensityLevel, EventType
)
from app.utils.auth import get_password_hash
from app.database import engine, Base, SessionLocal
from app.seeds.seed_data import (
    users, generate_daily_logs, generate_entries_for_log, 
    activity_recommendations
)

def seed_database():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Check if database is already seeded
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already has data. Skipping seeding.")
            return
        
        print("Seeding database...")
        
        # Seed users and profiles
        created_users = []
        for user_data in users:
            # Create user
            hashed_password = get_password_hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                is_active=True
            )
            db.add(user)
            db.flush()  # Get ID without committing
            
            # Create profile
            profile = Profile(
                user_id=user.id,
                bio=user_data.get("bio", None),
                timezone="UTC"
            )
            db.add(profile)
            created_users.append(user)
        
        db.commit()
        print(f"Created {len(created_users)} users with profiles")
        
        # Seed daily logs and entries
        for user in created_users:
            # Generate 14 days of logs
            logs_data = generate_daily_logs(user.id, num_days=14)
            
            created_logs = []
            for log_data in logs_data:
                log = DailyLog(
                    user_id=log_data["user_id"],
                    date=log_data["date"],
                    overall_mood=log_data["overall_mood"],
                    notes=log_data["notes"]
                )
                db.add(log)
                db.flush()  # Get ID without committing
                created_logs.append((log, log_data["date"], log_data["overall_mood"]))
            
            db.commit()
            print(f"Created {len(created_logs)} daily logs for user {user.username}")
            
            # Generate entries for each log
            for log, log_date, log_mood in created_logs:
                entries = generate_entries_for_log(log.id, log_date, log_mood)
                
                # Food entries
                for entry_data in entries["food_entries"]:
                    entry = FoodEntry(
                        daily_log_id=entry_data["daily_log_id"],
                        food_name=entry_data["food_name"],
                        meal_type=MealType(entry_data["meal_type"]),
                        calories=entry_data["calories"],
                        timestamp=entry_data["timestamp"]
                    )
                    db.add(entry)
                
                # Exercise entries
                for entry_data in entries["exercise_entries"]:
                    entry = ExerciseEntry(
                        daily_log_id=entry_data["daily_log_id"],
                        exercise_type=entry_data["exercise_type"],
                        description=entry_data["description"],
                        duration_minutes=entry_data["duration_minutes"],
                        intensity=IntensityLevel(entry_data["intensity"]),
                        calories_burned=entry_data["calories_burned"],
                        timestamp=entry_data["timestamp"]
                    )
                    db.add(entry)
                
                # Work entries
                for entry_data in entries["work_entries"]:
                    entry = WorkEntry(
                        daily_log_id=entry_data["daily_log_id"],
                        description=entry_data["description"],
                        start_time=entry_data["start_time"],
                        end_time=entry_data["end_time"],
                        productivity_rating=entry_data["productivity_rating"],
                        stress_level=entry_data["stress_level"]
                    )
                    db.add(entry)
                
                # Event entries
                for entry_data in entries["event_entries"]:
                    entry = EventEntry(
                        daily_log_id=entry_data["daily_log_id"],
                        description=entry_data["description"],
                        event_type=EventType(entry_data["event_type"]),
                        impact_rating=entry_data["impact_rating"],
                        timestamp=entry_data["timestamp"]
                    )
                    db.add(entry)
                
                # Mood entries
                for entry_data in entries["mood_entries"]:
                    entry = MoodEntry(
                        daily_log_id=entry_data["daily_log_id"],
                        mood_rating=entry_data["mood_rating"],
                        description=entry_data["description"],
                        timestamp=entry_data["timestamp"]
                    )
                    db.add(entry)
            
            db.commit()
            print(f"Created entries for user {user.username}")
            
            # Add activity recommendations for each user
            for i in range(2):  # Add 2 recommendations per user
                rec_data = random.choice(activity_recommendations)
                recommendation = ActivityRecommendation(
                    user_id=user.id,
                    activity_name=rec_data["activity_name"],
                    description=rec_data["description"],
                    duration_minutes=rec_data["duration_minutes"],
                    expected_benefit=rec_data["expected_benefit"],
                    is_completed=random.choice([True, False])
                )
                
                if recommendation.is_completed:
                    recommendation.user_rating = random.randint(1, 5)
                
                db.add(recommendation)
            
            db.commit()
            print(f"Added activity recommendations for user {user.username}")
            
        print("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()