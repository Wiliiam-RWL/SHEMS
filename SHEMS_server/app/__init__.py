from flask import Flask
from app.routes import init_app
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.db import database


def create_app():
    app = Flask(__name__)
    init_app(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    app.config['JWT_SECRET_KEY'] = 'schems'  # Change this to a random secret key
    jwt = JWTManager(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        database.Database.close_session()

    return app
