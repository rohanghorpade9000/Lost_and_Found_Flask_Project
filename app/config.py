import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

# Configure MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/lostfound_db")
client = MongoClient(MONGO_URI)
db = client.get_database()

# Define collections
lost_items = db["lost_items"]
found_items = db["found_items"]
users = db["users"]  # New collection for storing registered users
