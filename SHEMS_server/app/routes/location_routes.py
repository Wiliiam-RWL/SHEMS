from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import (
    get_customer_location,
    add_location,
    modify_location,
    delete_location,
)
from ..db.database import Database
from sqlalchemy import text

location_blueprint = Blueprint("location", __name__)


@location_blueprint.route("/all", methods=["GET"])
@jwt_required()
def getLocation1():
    email = get_jwt_identity()
    locations = get_customer_location(email)
    return jsonify(locations), 200


@location_blueprint.route("/add", methods=["POST"])
@jwt_required()
def addLocation():
    data = request.get_json()
    success = add_location(data)
    if success == True:
        return jsonify({"success": success}, 201)
    else:
        return jsonify({"success": success}, 400)


@location_blueprint.route("/modify", methods=["PUT"])
@jwt_required()
def modifyLocation():
    data = request.get_json()
    location_id = data.get("location_id")
    square_feet = data.get("square_feet")
    num_bedrooms = data.get("num_bedrooms")
    num_occupants = data.get("num_occupants")

    success = modify_location(location_id, num_bedrooms, num_occupants, square_feet)

    if success == True:
        return jsonify({"success": success}, 201)
    else:
        return jsonify({"success": success}, 400)


@location_blueprint.route("/delete", methods=["PUT"])
@jwt_required()
def deleteLocation():
    data = request.get_json()
    location_id = data.get("location_id")
    print(data)
    success = delete_location(location_id=location_id)
    if success == True:
        return jsonify({"success": success}, 201)
    else:
        return jsonify({"success": success}, 400)
