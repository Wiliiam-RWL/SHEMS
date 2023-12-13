from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import get_customer_location, get_customer_id
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
    customer_id = get_customer_id(data.get("email"))
    start_date = "2022-07-31 23:59:59"
    sql_string = (
        "INSERT INTO location("
        "customer_id, "
        "location_street_num, "
        "location_street_name, "
        "location_unit_number, "
        "location_city, "
        "location_state, "
        "location_zipcode, "
        "square_feet, "
        "num_bedrooms, "
        "num_occupants, "
        "start_date) VALUES "
        "(%s, %s, '%s', '%s', '%s', '%s', '%s', %s, %s, %s, '%s')"
    )

    sql = text(
        sql_string
        % (
            customer_id,
            data.get("location_street_num"),
            data.get("location_street_name"),
            data.get("location_unit_number"),
            data.get("location_city"),
            data.get("location_state"),
            data.get("location_zip_code"),
            data.get("square_feet"),
            data.get("num_bedrooms"),
            data.get("num_occupants"),
            start_date,  # Make sure this is a valid datetime string
        )
    )

    success = Database.handle_transaction([{"query": sql, "params": None}])

    return jsonify({"success": success}, 201)
