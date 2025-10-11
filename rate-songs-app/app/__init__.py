import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

def create_app() -> Flask:
    load_dotenv()

    application = Flask(__name__, template_folder="templates", static_folder="static")
    application.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me")

    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB_NAME", "rate_songs_dev")

    if not mongo_uri:
        raise RuntimeError("MONGO_URI is missing from environment variables.")

    # Connect to MongoDB (with TLS)
    client = MongoClient(mongo_uri, tls=True)
    application.db = client[mongo_db_name]

    # Quick connection test
    try:
        application.db.command("ping")
        print(f"✅ Connected to MongoDB database: {mongo_db_name}")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")

    # register home blueprint (follow similar pattern for other blueprints)
    from .routes.home import home_bp    
    application.register_blueprint(home_bp)

    return application
