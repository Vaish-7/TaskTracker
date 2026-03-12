from flask import Flask
from .db import db
from flask_jwt_extended import JWTManager
from .errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task-timer-tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'dev-jwt-secret'
    app.config['SECRET_KEY'] = 'dev-session-secret'

    db.init_app(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    from .routes import bp
    app.register_blueprint(bp)

    register_error_handlers(app)

    return app
