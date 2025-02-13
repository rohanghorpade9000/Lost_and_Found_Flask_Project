# Lost_and_Found_Flask_Project

📌 Overview
This is a Lost & Found Management System API built using Flask and MongoDB.
It allows users to:

📢 Report lost & found items (with images).
🔍 Automatically match items based on fuzzy logic.
📩 Notify users via email when their lost item is found.
✨ Features
✔️ User Authentication (JWT-based login & registration)
✔️ Report Lost & Found Items (with image upload)
✔️ 🔔 Automated Email Notifications when a match is found
✔️ 📍 Nearby Lost Item Search
✔️ 🛡️ Secure API Endpoints (JWT Token Required)
✔️ 🖼️ Cloud Storage for Images (via Cloudinary)
✔️ 🐳 Dockerized MongoDB Setup

🏗️ Tech Stack
🖥️ Backend: Flask, Flask-PyMongo, JWT
📦 Database: MongoDB (via Docker)
🖼️ Image Storage: Cloudinary
🔐 Authentication: JWT (JSON Web Tokens)
⏳ Task Scheduling: Celery (Optional for Future Enhancements)
🐳 Containerization: Docker (docker-compose for MongoDB)

🚀 Setup & Installation
🔹 1. Clone the Repository

sh
git clone https://github.com/rohanghorpade9000/Lost_and_Found_Flask_Project.git
cd Lost_and_Found_Flask_Project

🔹 2. Create a Virtual Environment & Install Dependencies

sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
pip install -r requirements.txt

🔹 3. Setup Environment Variables
Create a .env file in the root directory and add:

ini
MONGO_URI=mongodb://localhost:27017/lostfound_db
SECRET_KEY=your_secret_key_here
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_email_password

🔹 4. Start MongoDB using Docker

sh
docker-compose up -d

🔹 5. Run the Application

sh
python run.py
🚀 Your API is now running at http://127.0.0.1:5000/

📡 API Endpoints

🔐 Authentication (Users)

POST   /users/register       # Register a new user
POST   /users/login          # Login & get JWT token

📢 Lost & Found Items

POST   /lost-items/                  # Report a lost item
POST   /found-items/                 # Report a found item
GET    /lost-items/                  # Get all lost items
GET    /found-items/                 # Get all found items
DELETE /lost-items/{id}              # Delete a lost item (owner only)
DELETE /found-items/{id}             # Delete a found item (owner only)
PUT    /found-items/claim/{id}       # Claim a found item
POST   /lost-items/upload-image      # Upload an image for lost item
POST   /found-items/upload-image     # Upload an image for found item

🔍 Matching & Search

GET    /match-items/                          # Match lost items with found items
GET    /nearby-lost-items?location=xyz        # Find lost items nearby

🔒 Authentication Header Format

All protected routes require a JWT token in the Authorization header:
Authorization: Bearer YOUR_JWT_TOKEN
