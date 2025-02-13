import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(image_file, public_id=None):
    """Uploads an image to Cloudinary and returns the secure URL."""
    upload_options = {"public_id": public_id} if public_id else {}
    result = cloudinary.uploader.upload(image_file, **upload_options)
    return result["secure_url"]
