# app/routes/__init__.py

from flask import Flask
from .auth_routes import auth_blueprint
from .location_routes import location_blueprint
from .customer_routes import customer_blueprint
from .device_routes import device_blueprint

def init_app(app: Flask):
    app.register_blueprint(auth_blueprint , url_prefix='/auth')
    app.register_blueprint(location_blueprint , url_prefix='/location')
    app.register_blueprint(customer_blueprint , url_prefix='/customer')
    app.register_blueprint(device_blueprint , url_prefix='/device')