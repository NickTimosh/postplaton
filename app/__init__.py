from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Database configuration
    db_path = os.path.join(app.instance_path, "events.db")
    db_path = db_path.replace("\\", "/")

    # Set SQLAlchemy database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key") 

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = "login"  # endpoint for @login_required redirects
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes
    from app.routes.home import home_bp
    from app.routes.events import events_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(auth_bp)

    return app

