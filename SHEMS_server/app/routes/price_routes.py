from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import (
    get_price_of_locations,
    get_customer_id,
    get_price_of_each_device_type,
get_price_by_customer_per_day
)

price_blueprint = Blueprint("price", __name__)


@price_blueprint.route("/location/pie", methods=["GET"])
@jwt_required()
def getCostByLocation():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
    res = get_price_of_locations(customer_id, start, end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200


@price_blueprint.route("/device-type", methods=["GET"])
@jwt_required()
def getCostByDeviceType():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
    res = get_price_of_each_device_type(customer_id, start, end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200


@price_blueprint.route("/customer/day", methods=["GET"])
@jwt_required()
def getPriceOfCustomerPerDay():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
    res = get_price_by_customer_per_day(customer_id,start,end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200