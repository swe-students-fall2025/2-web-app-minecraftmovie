import os
from flask import Flask
from dotenv import load_dotenv

def create_app() -> Flask:
    load_dotenv()

    application = Flask(__name__, template_folder="templates", static_folder="static")
    application.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me")

    # register home blueprint (follow similar pattern for other blueprints)
    from .routes.home import home_bp    
    application.register_blueprint(home_bp)

    return application
