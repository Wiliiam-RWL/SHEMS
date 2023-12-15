from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import (
    get_energy_by_customer_per_day,
    get_energy_by_customer_per_month,
    get_customer_id,
)
from datetime import datetime

energy_blueprint = Blueprint("energy", __name__)


@energy_blueprint.route("/test", methods=["GET"])
def test():
    customer_id = 2
    start = datetime.strptime("2022-08-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime("2022-12-31 00:00:00", "%Y-%m-%d %H:%M:%S")
    per_day = get_energy_by_customer_per_day(customer_id, start, end)
    per_month = get_energy_by_customer_per_month(customer_id, start, end)
    return jsonify(per_day), 200


@energy_blueprint.route("/customer/day", methods=["GET"])
@jwt_required()
def getEnergyPerDay():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")

    per_day = get_energy_by_customer_per_day(customer_id, start, end)
    if per_day is not None:
        return jsonify(per_day), 200
    else:
        return jsonify(None, 400)
