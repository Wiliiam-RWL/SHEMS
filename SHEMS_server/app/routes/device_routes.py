from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import get_customer_device

device_blueprint = Blueprint('device', __name__)


@device_blueprint.route('/all', methods=['GET'])
@jwt_required()
def getAllDevices():
    email = get_jwt_identity()
    locations = get_customer_device(email)
    return jsonify(locations), 200


@device_blueprint.route('/add', methods=['POST'])
@jwt_required()
def addNewDevice():
    data = request.get_json()
    location_id = data.get('location_id')
    model_id = data.get('model_id')
    tag = data.get('tag')

    return 0, 200
