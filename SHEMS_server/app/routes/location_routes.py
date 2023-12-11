from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services import get_customer_location
location_blueprint = Blueprint('location', __name__)

@location_blueprint.route('/all', methods=['GET'])
@jwt_required()
def getLocation1():
    email = get_jwt_identity()
    locations = get_customer_location(email)
    return jsonify(locations), 200

