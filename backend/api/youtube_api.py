from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_service():
    if not API_KEY:
        raise ValueError("API key not found. Check your .env file")

    youtube = build(
        serviceName="youtube",
        version="v3",
        developerKey=API_KEY
    )
    return youtube
