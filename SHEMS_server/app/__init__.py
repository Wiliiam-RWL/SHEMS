from flask import Flask
from app.routes import init_app
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    init_app(app)
    app.config['JWT_SECRET_KEY'] = 'schems'  # Change this to a random secret key
    jwt = JWTManager(app)

    return app
