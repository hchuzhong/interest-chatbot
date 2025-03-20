# filepath: /Users/hchuzhong/Desktop/daai-course/7940/group project/chatbot/chatbot.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Telegram access token
TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")

if not TELEGRAM_ACCESS_TOKEN:
    raise ValueError("Telegram access token not found. Please set it in the .env file.")


print('TELEGRAM_ACCESS_TOKEN:', TELEGRAM_ACCESS_TOKEN)