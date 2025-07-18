from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
import os
from .config import Config
from .firebase_auth import firebase_auth_required
from flask import request
from flask_migrate import Migrate
# import app.models

db = SQLAlchemy()
redis_client = None  # Will initialize later
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)

    migrate.init_app(app, db)
    from app.models import Bus, Booking

    # Set up Redis client (as a global)
    global redis_client
    redis_client = redis.Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        decode_responses=True  # Converts bytes to str
    )

    # Temporary test route
    @app.route("/health")
    def health_check():
        return {"status": "ok"}, 200
    
    @app.route("/user/me")
    @firebase_auth_required
    def get_current_user():
        user = request.user
        return {
            "uid": user["uid"],
            "email": user.get("email"),
        }, 200
    
    from app.routes.bus_routes import bus_bp
    app.register_blueprint(bus_bp)


    return app
