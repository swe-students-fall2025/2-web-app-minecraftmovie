from .auth import auth_bp
from .home import home_bp
from .profile import profile_bp
from .songs import songs_bp
from .upload import upload_bp

def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(songs_bp)  
    app.register_blueprint(upload_bp) 

