from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import get_customer_device, get_all_device_model, add_device, delete_device

device_blueprint = Blueprint('device', __name__)


@device_blueprint.route('/all', methods=['GET'])
@jwt_required()
def getAllDevices():
    email = get_jwt_identity()
    locations = get_customer_device(email)
    return jsonify(locations), 200


@device_blueprint.route('/model/all', methods=['GET'])
@jwt_required()
def getAllDeviceModels():
    models = get_all_device_model()
    return jsonify(models), 200

@device_blueprint.route('/add', methods=['POST'])
@jwt_required()
def addNewDevice():
    data = request.get_json()
    location_id = data.get('location_id')
    model_id = data.get('model_id')
    tag = data.get('tag')
    success = add_device(location_id, model_id, tag)
    if success:
        return jsonify({"success": success}), 201
    else:
        return jsonify({"success": success}), 400


@device_blueprint.route('/delete', methods=['POST'])
@jwt_required()
def deleteDevice():
    data = request.get_json()
    device_id = data.get('device_id')
    success = delete_device(device_id)
    if success:
        return jsonify({"success": success}), 200
    else:
        return jsonify({"success": success}), 400