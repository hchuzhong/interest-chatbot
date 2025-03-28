import json
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Interest categories for both users and events
INTERESTS = [
    "online gaming", "VR experiences", "social media groups", "swimming",
    "coding", "music streaming", "virtual art galleries", "e-sports",
    "cooking", "online shopping", "yoga", "reading", "podcasts",
    "gardening", "DIY projects", "travel", "photography", "biking",
    "hiking", "running", "meditation", "painting", "dancing", "movies",
    "board games", "fashion", "sports", "pets", "food", "coffee",
    "tea", "beer", "wine", "cocktails", "juices", "smoothies", "desserts",
    "badminton", "basketball", "football", "tennis", "volleyball", "golf",
    "table tennis", "chess", "poker", "billiards", "darts", "bowling",
]

# --- Generate 500 Users for user ---
def generate_user_data():
    users = []
    for i in range(500):
        base = random.randint(100000000, 999999999)  # 9-digit number
        telegram_id = str(base + i)  # Simple unique Telegram IDs
        username = fake.user_name()
        num_interests = random.randint(1, 3)  # 1-3 interests per user
        interests = random.sample(INTERESTS, num_interests)
        last_updated = fake.date_time_between(start_date="-30d", end_date="now").isoformat() + "Z"
        
        user = {
            "telegramId": telegram_id,
            "username": username,
            "interests": interests,
            "lastUpdated": last_updated
        }
        users.append(user)
    return users

# --- Generate 100 Events for events ---
def generate_event_data():
    events = []
    for i in range(100):
        event_id = f"EVT{str(i+1).zfill(3)}"  # e.g., EVT001, EVT002
        event_type = random.choice(INTERESTS)
        name = f"{event_type.replace('_', ' ').title()} {random.choice(['Meetup', 'Tournament', 'Workshop', 'Hangout', 'Session', 'Event'])}"
        date = fake.date_time_between(start_date="now", end_date="+30d").isoformat() + "Z"
        description = fake.sentence(nb_words=6)
        participants = random.randint(5, 50)
        
        event = {
            "eventId": event_id,
            "name": name,
            "type": event_type,
            "date": date,
            "description": description,
            "participants": participants
        }
        events.append(event)
    return events

# Generate the data
user_data = generate_user_data()
event_data = generate_event_data()

# Export to JSON files
with open("user.json", "w") as user_file:
    json.dump(user_data, user_file, indent=4)

with open("events.json", "w") as event_file:
    json.dump(event_data, event_file, indent=4)

print("Generated and exported 500 users to 'user.json' and 100 events to 'events.json'.")