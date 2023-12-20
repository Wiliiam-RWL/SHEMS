from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import (
    get_energy_by_customer_per_day,
    get_energy_by_customer_per_month,
    get_customer_id,
    get_energy_by_device_type,
    get_energy_by_location_id,
    get_customer_energy_per_locatoin,
    get_energy_of_all_devices,
    get_energy_of_all_device_per_day,
    get_energy_by_location_device_type,
)
from datetime import datetime

energy_blueprint = Blueprint("energy", __name__)


@energy_blueprint.route("/test", methods=["GET"])
def test():
    customer_id = 2
    start = datetime.strptime("2022-08-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime("2022-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")
    per_location_day = get_customer_energy_per_locatoin(customer_id, start, end)
    return jsonify(per_location_day), 200


@energy_blueprint.route("/location", methods=["GET"])
@jwt_required()
def getEnergyPerLocationPerDay():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    per_location_per_day = get_customer_energy_per_locatoin(customer_id, start, end)
    print(per_location_per_day)
    if per_location_per_day is not None:
        return jsonify(per_location_per_day), 200
    else:
        return jsonify(None), 200


@energy_blueprint.route("/customer/day", methods=["GET"])
@jwt_required()
def getEnergyPerDay():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    per_day = get_energy_by_customer_per_day(customer_id, start, end)
    if per_day is not None:
        return jsonify(per_day), 200
    else:
        return jsonify(None, 400)


@energy_blueprint.route("/device/type", methods=["GET"])
@jwt_required()
def getEnergyByDeviceType():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    res = get_energy_by_device_type(customer_id, start, end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200


@energy_blueprint.route("/location/device_type", methods=["GET"])
@jwt_required()
def getEnergyByLocationDeviceType():
    # Retrieve 'start' and 'end' from the query parameters
    location_id = request.args.get("location_id")
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    res = get_energy_by_location_device_type(location_id, start, end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200


@energy_blueprint.route("/location/pie", methods=["GET"])
@jwt_required()
def getEnergyByLocation():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    res = get_energy_by_location_id(customer_id, start, end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200


@energy_blueprint.route("/device/all", methods=["GET"])
@jwt_required()
def getEnergyOfAllDevices():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")

    res = get_energy_of_all_devices(customer_id, start, end)
    if res is not None:
        return jsonify(res), 200
    else:
        return jsonify([]), 200


@energy_blueprint.route("/device/day", methods=["GET"])
@jwt_required()
def getEnergyPerDayByDeviceID():
    email = get_jwt_identity()
    customer_id = get_customer_id(email=email)

    # Retrieve 'start' and 'end' from the query parameters
    start = request.args.get("start")
    end = request.args.get("end")
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
    device_id = request.args.get("device_id")

    per_day = get_energy_of_all_device_per_day(customer_id, device_id, start, end)
    if per_day is not None:
        return jsonify(per_day), 200
    else:
        return jsonify([]), 200
