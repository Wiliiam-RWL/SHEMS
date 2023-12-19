# app/routes/__init__.py

from flask import Flask
from .auth_routes import auth_blueprint
from .location_routes import location_blueprint
from .customer_routes import customer_blueprint
from .device_routes import device_blueprint
from .energy_routes import energy_blueprint
from .price_routes import price_blueprint


def init_app(app: Flask):
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(location_blueprint, url_prefix="/location")
    app.register_blueprint(customer_blueprint, url_prefix="/customer")
    app.register_blueprint(device_blueprint, url_prefix="/device")
    app.register_blueprint(energy_blueprint, url_prefix="/energy")
    app.register_blueprint(price_blueprint, url_prefix="/price")
