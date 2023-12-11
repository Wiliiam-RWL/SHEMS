from ..services import get_user_info
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

customer_blueprint = Blueprint("customer", __name__)
@customer_blueprint.route('/info', methods=['GET'])
@jwt_required()
def getCustomerInfo():
    email = get_jwt_identity()
    info = get_user_info(email)
    print(info)
    return jsonify(info), 200
