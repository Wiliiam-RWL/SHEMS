# app/routes/__init__.py

from flask import Flask
from .auth_routes import auth_blueprint

def init_app(app: Flask):
    app.register_blueprint(auth_blueprint , url_prefix='/auth')
