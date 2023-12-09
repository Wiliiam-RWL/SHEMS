from flask import Blueprint,request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

location_blueprint = Blueprint('location', __name__)

@location_blueprint.route('/test', methods=['GET'])
@jwt_required()
def getLocation1():
    email = get_jwt_identity()
    print(email)
    return jsonify({'success': True, 'message': 'Test successful'}), 200



@location_blueprint.route('/test1', methods=['GET'])
def getLocation():
    email = request.get_json().get('email')
    print(email)
    return jsonify({'success': True, 'message': 'Test successful'}), 200