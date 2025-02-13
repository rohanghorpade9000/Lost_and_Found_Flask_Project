from flask import Flask
from app.config import db
from app.routes import init_routes

def create_app():
    app = Flask(__name__)

    # Initialize Routes
    init_routes(app)

    return app
