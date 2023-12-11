from ..services import check_user_credentials, register_user
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    billing_street_num = data.get("billing_street_num")
    billing_street_name = data.get("billing_street_name")
    billing_unit_number = data.get("billing_unit_number")
    billing_city = data.get("billing_city")
    billing_state = data.get("billing_state")
    billing_zipcode = data.get("billing_zipcode")

    success, message = register_user(
        first_name,
        last_name,
        email,
        password,
        billing_street_num,
        billing_street_name,
        billing_unit_number,
        billing_city,
        billing_state,
        billing_zipcode,
    )

    if success:
        return jsonify({"success": True, "message": message}), 201
    else:
        return jsonify({"success": False, "message": message}), 400


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # You should add additional validation for the input data here

    if check_user_credentials(email, password):
        access_token = create_access_token(identity=email)
        return (
            jsonify(
                {
                    "success": True,
                    "message": "Login successful",
                    "token": access_token,
                    "email": email,
                }
            ),
            200,
        )
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
