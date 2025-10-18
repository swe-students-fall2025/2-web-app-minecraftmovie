# app/__init__.py
import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from flask_login import LoginManager
from bson import ObjectId
from app.models import UserDoc

load_dotenv()

login_manager = LoginManager()
mongo_client = None
mongo_db = None

def create_app() -> Flask:
    load_dotenv()

    application = Flask(__name__, template_folder="templates", static_folder="static")
    application.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me")

    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME", "rate_songs_dev")

    if not mongo_uri:
        raise RuntimeError("MONGO_URI is missing from environment variables.")

    # Connect to MongoDB (with TLS)
    global mongo_client, mongo_db
    mongo_client = MongoClient(mongo_uri, tls=True)
    mongo_db = mongo_client[mongo_db_name]
    application.db = mongo_db

    #
    mongo_db.users.create_index("email", unique=True)

    # Flask-Login
    login_manager.init_app(application)
    login_manager.login_view = "auth.login"

    # Register blueprints
    from .routes.home import home_bp
    from .routes.auth import auth_bp
    from .routes.profile import profile_bp
    from .routes.songs import songs_bp
    from .routes.upload import upload_bp
    from .routes.edit import edit_bp
    from .routes.delete import delete_bp

    application.register_blueprint(home_bp)
    application.register_blueprint(auth_bp)
    application.register_blueprint(profile_bp)
    application.register_blueprint(songs_bp)
    application.register_blueprint(upload_bp)
    application.register_blueprint(edit_bp)
    application.register_blueprint(delete_bp)

    return application

@login_manager.user_loader
def load_user(user_id: str):
    if not user_id:
        return None
    try:
        doc = mongo_db.users.find_one({"_id": ObjectId(user_id)})
        return UserDoc(doc) if doc else None
    except Exception:
        return None
