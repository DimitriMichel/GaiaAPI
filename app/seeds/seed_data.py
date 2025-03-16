# app/seeds/seed_data.py
from datetime import datetime, timedelta
import random
from typing import List, Dict

# User seed data
users = [
    {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "password123",
        "bio": "Fitness enthusiast and healthy eating advocate."
    },
    {
        "username": "janedoe",
        "email": "jane@example.com",
        "password": "password123",
        "bio": "Working professional trying to maintain work-life balance."
    },
    {
        "username": "samsmith",
        "email": "sam@example.com",
        "password": "password123",
        "bio": "Musician and night owl. Working on better sleep habits."
    }
]

# Regular food entries
food_types = [
    {"name": "Oatmeal with berries", "meal_type": "breakfast", "calories": 320},
    {"name": "Greek yogurt with honey", "meal_type": "breakfast", "calories": 220},
    {"name": "Avocado toast", "meal_type": "breakfast", "calories": 350},
    {"name": "Chicken salad", "meal_type": "lunch", "calories": 450},
    {"name": "Veggie wrap", "meal_type": "lunch", "calories": 380},
    {"name": "Quinoa bowl", "meal_type": "lunch", "calories": 420},
    {"name": "Salmon with vegetables", "meal_type": "dinner", "calories": 520},
    {"name": "Pasta with tomato sauce", "meal_type": "dinner", "calories": 560},
    {"name": "Stir-fry with tofu", "meal_type": "dinner", "calories": 480},
    {"name": "Apple", "meal_type": "snack", "calories": 95},
    {"name": "Protein bar", "meal_type": "snack", "calories": 180},
    {"name": "Mixed nuts", "meal_type": "snack", "calories": 210}
]

# Problematic food that causes bloating
bloating_foods = [
    {"name": "Dairy-heavy pizza", "meal_type": "dinner", "calories": 850},
    {"name": "Cheesy pasta", "meal_type": "dinner", "calories": 780},
    {"name": "Ice cream sundae", "meal_type": "snack", "calories": 450},
    {"name": "Milkshake", "meal_type": "snack", "calories": 520},
]

# Exercise entries
exercise_types = [
    {"type": "Running", "intensity": "moderate", "calories_burned": 350},
    {"type": "Cycling", "intensity": "high", "calories_burned": 500},
    {"type": "Swimming", "intensity": "high", "calories_burned": 450},
    {"type": "Yoga", "intensity": "low", "calories_burned": 200},
    {"type": "Weight training", "intensity": "moderate", "calories_burned": 300},
    {"type": "HIIT workout", "intensity": "very_high", "calories_burned": 450},
    {"type": "Walking", "intensity": "low", "calories_burned": 150},
    {"type": "Pilates", "intensity": "moderate", "calories_burned": 250},
    {"type": "Dancing", "intensity": "moderate", "calories_burned": 280}
]

# Work entries
work_descriptions = [
    "Focused deep work session",
    "Team meetings",
    "Administrative tasks",
    "Client presentations",
    "Email and communication",
    "Project planning",
    "Learning and development",
    "Brainstorming session"
]

# Event types
events = [
    {"description": "Dinner with friends", "event_type": "social", "impact_rating": 3},
    {"description": "Family gathering", "event_type": "social", "impact_rating": 4},
    {"description": "Doctor's appointment", "event_type": "health", "impact_rating": 0},
    {"description": "Work deadline", "event_type": "professional", "impact_rating": -2},
    {"description": "Job promotion", "event_type": "professional", "impact_rating": 5},
    {"description": "Argument with partner", "event_type": "personal", "impact_rating": -3},
    {"description": "Relaxing weekend", "event_type": "personal", "impact_rating": 4},
    {"description": "Meditation session", "event_type": "health", "impact_rating": 2},
    {"description": "Volunteering", "event_type": "social", "impact_rating": 3},
    {"description": "Movie night", "event_type": "social", "impact_rating": 2}
]

# Regular mood descriptions
mood_descriptions = [
    "Feeling energetic and positive",
    "Stressed but managing",
    "Tired but content",
    "Anxious about work",
    "Happy and relaxed",
    "Overwhelmed with responsibilities",
    "Motivated and focused",
    "Calm and centered",
    "Irritable and restless",
    "Satisfied and accomplished"
]

# Mood descriptions specifically after dairy consumption
dairy_mood_descriptions = [
    "Feeling bloated and uncomfortable",
    "Stomach discomfort after eating",
    "Digestive issues affecting my mood",
    "Feeling sluggish after meal",
    "Uncomfortable digestive symptoms"
]

# Activity recommendations
activity_recommendations = [
    {
        "activity_name": "Morning meditation",
        "description": "Start your day with 10 minutes of mindfulness meditation to center yourself and prepare for the day ahead.",
        "duration_minutes": 10,
        "expected_benefit": "Reduced stress and improved focus"
    },
    {
        "activity_name": "Nature walk",
        "description": "Take a walk in a natural setting, paying attention to the sights, sounds, and sensations around you.",
        "duration_minutes": 30,
        "expected_benefit": "Mood improvement and stress reduction"
    },
    {
        "activity_name": "Digital detox",
        "description": "Set aside time without screens to read, reflect, or engage in a hobby.",
        "duration_minutes": 60,
        "expected_benefit": "Mental clarity and reduced anxiety"
    },
    {
        "activity_name": "Gratitude journaling",
        "description": "Write down three things you're grateful for today, with specific details about why they matter to you.",
        "duration_minutes": 15,
        "expected_benefit": "Improved positive outlook and emotional well-being"
    },
    {
        "activity_name": "Social connection",
        "description": "Reach out to a friend or family member you haven't spoken to recently for a meaningful conversation.",
        "duration_minutes": 20,
        "expected_benefit": "Enhanced sense of belonging and emotional support"
    }
]

def generate_daily_logs(user_id: int, num_days: int = 14) -> List[Dict]:
    """Generate a series of daily logs for a user"""
    logs = []
    end_date = datetime.now().replace(hour=20, minute=0, second=0, microsecond=0)
    
    for i in range(num_days):
        log_date = end_date - timedelta(days=i)
        
        # Overall mood tends to be influenced by recent events and lifestyle factors
        # This is a simplified model but creates some realistic patterns
        base_mood = random.randint(5, 8)  # Base mood between 5-8
        
        # Add some variability for weekends
        if log_date.weekday() >= 5:  # Weekend
            base_mood += random.randint(0, 2)  # Weekend mood boost
        
        # Add some random variation
        mood_adjustment = random.randint(-2, 2)
        overall_mood = max(1, min(10, base_mood + mood_adjustment))  # Keep within 1-10 range
        
        # If this is a day the user typically eats dairy (Tuesday and Friday), reduce mood
        if log_date.weekday() in [1, 4]:
            overall_mood = max(1, overall_mood - random.randint(1, 2))
        
        logs.append({
            "user_id": user_id,
            "date": log_date,
            "overall_mood": overall_mood,
            "notes": f"Day {num_days - i} of tracking"
        })
    
    return logs

def generate_entries_for_log(log_id: int, log_date: datetime, log_mood: int) -> Dict:
    """Generate entries for a specific log"""
    entries = {
        "food_entries": [],
        "exercise_entries": [],
        "work_entries": [],
        "event_entries": [],
        "mood_entries": []
    }
    
    # Determine if today is a dairy day (Tuesday and Friday)
    is_dairy_day = log_date.weekday() in [1, 4]
    
    # Add 3-5 food entries
    num_food_entries = random.randint(3, 5)
    for _ in range(num_food_entries):
        # Choose regular food
        food = random.choice(food_types)
        hour = random.choice([7, 8, 12, 13, 18, 19, 15, 16])  # Appropriate hours for meals
        timestamp = log_date.replace(hour=hour, minute=random.randint(0, 59))
        
        entries["food_entries"].append({
            "daily_log_id": log_id,
            "food_name": food["name"],
            "meal_type": food["meal_type"],
            "calories": food["calories"],
            "timestamp": timestamp
        })
    
    # Add a dairy food on Tuesday and Friday evenings
    if is_dairy_day:
        dairy_food = random.choice(bloating_foods)
        dinner_hour = random.randint(18, 20)
        timestamp = log_date.replace(hour=dinner_hour, minute=random.randint(0, 59))
        
        entries["food_entries"].append({
            "daily_log_id": log_id,
            "food_name": dairy_food["name"],
            "meal_type": dairy_food["meal_type"],
            "calories": dairy_food["calories"],
            "timestamp": timestamp
        })
        
        # Add a mood entry about bloating 1-2 hours after dairy consumption
        post_dairy_hour = min(23, dinner_hour + random.randint(1, 2))
        post_dairy_mood = max(1, log_mood - random.randint(2, 3))
        
        entries["mood_entries"].append({
            "daily_log_id": log_id,
            "mood_rating": post_dairy_mood,
            "description": random.choice(dairy_mood_descriptions),
            "timestamp": log_date.replace(hour=post_dairy_hour, minute=random.randint(0, 59))
        })
    
    # Add 0-2 exercise entries
    num_exercise_entries = random.randint(0, 2)
    for _ in range(num_exercise_entries):
        exercise = random.choice(exercise_types)
        hour = random.choice([6, 7, 17, 18, 19])  # Common exercise hours
        timestamp = log_date.replace(hour=hour, minute=random.randint(0, 59))
        duration = random.randint(20, 60)
        
        entries["exercise_entries"].append({
            "daily_log_id": log_id,
            "exercise_type": exercise["type"],
            "description": f"{duration} minute {exercise['type']} session",
            "duration_minutes": duration,
            "intensity": exercise["intensity"],
            "calories_burned": round(exercise["calories_burned"] * duration / 30),  # Adjust for duration
            "timestamp": timestamp
        })
    
    # Add work entries for weekdays
    if log_date.weekday() < 5:  # Weekday
        work_desc = random.choice(work_descriptions)
        start_hour = random.randint(8, 10)
        work_duration = random.randint(6, 9)  # Hours of work
        
        # Productivity and stress inversely correlate with mood somewhat
        productivity = random.randint(max(1, log_mood - 3), min(10, log_mood + 3))
        stress = random.randint(max(1, 11 - log_mood - 3), min(10, 11 - log_mood + 3))
        
        entries["work_entries"].append({
            "daily_log_id": log_id,
            "description": work_desc,
            "start_time": log_date.replace(hour=start_hour, minute=0),
            "end_time": log_date.replace(hour=start_hour + work_duration, minute=0),
            "productivity_rating": productivity,
            "stress_level": stress
        })
    
    # Add 0-2 event entries
    num_event_entries = random.randint(0, 2)
    for _ in range(num_event_entries):
        event = random.choice(events)
        hour = random.randint(8, 21)  # Events can happen throughout the day
        timestamp = log_date.replace(hour=hour, minute=random.randint(0, 59))
        
        entries["event_entries"].append({
            "daily_log_id": log_id,
            "description": event["description"],
            "event_type": event["event_type"],
            "impact_rating": event["impact_rating"],
            "timestamp": timestamp
        })
    
    # Add 1-3 regular mood entries
    num_mood_entries = random.randint(1, 3)
    for i in range(num_mood_entries):
        hour = 8 + i * 6  # Spread through the day
        mood_rating = max(1, min(10, log_mood + random.randint(-2, 2)))  # Variation from daily average
        
        entries["mood_entries"].append({
            "daily_log_id": log_id,
            "mood_rating": mood_rating,
            "description": random.choice(mood_descriptions),
            "timestamp": log_date.replace(hour=hour, minute=random.randint(0, 59))
        })
    
    return entries