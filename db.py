import os
from pymongo import MongoClient

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get MongoDB URI from environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    raise ValueError("Please define the MONGODB_URI environment variable in the .env file.")

# Connect to MongoDB
def connect_to_db():
    client = MongoClient(MONGODB_URI)
    db = client['userInterestsDB']
    return db, client