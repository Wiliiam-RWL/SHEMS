from werkzeug.security import generate_password_hash, check_password_hash
from ..db.database import Database
from sqlalchemy import text



def register_user(first_name, last_name, email, password, billing_street_num, billing_street_name, billing_unit_number, billing_city, billing_state, billing_zipcode):
    """
    Registers a new customer by inserting their details into the database.
    Checks if the email already exists before proceeding.

    :param first_name: Customer's first name
    :param last_name: Customer's last name
    :param email: Customer's email
    :param password: Customer's plain-text password
    :param billing_street_num: Customer's billing street number
    :param billing_street_name: Customer's billing street name
    :param billing_unit_number: Customer's billing unit number
    :param billing_city: Customer's billing city
    :param billing_state: Customer's billing state
    :param billing_zipcode: Customer's billing zipcode
    :return: Success or failure message
    """
    # Check if the email already exists
    sql_check = text("SELECT COUNT(*) FROM customer WHERE email = :email")
    result = Database.execute_query(sql_check, {'email': email}).fetchone()

    if result[0] > 0:
        return False,"Email already exists."

    # Proceed with registration if email is not taken
    print(password)
    hashed_password = generate_password_hash(password,method='pbkdf2:sha256')
    print(hashed_password)

    sql_insert = text(
        """
        INSERT INTO customer (
            first_name, last_name, email, cpassword, billing_street_num, 
            billing_street_name, billing_unit_number, billing_city, billing_state, billing_zipcode
        ) VALUES (
            :first_name, :last_name, :email, :cpassword, :billing_street_num, 
            :billing_street_name, :billing_unit_number, :billing_city, :billing_state, :billing_zipcode
        )
        """
    )

    # Pass parameters as a dictionary
    params = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'cpassword': hashed_password,
        'billing_street_num': billing_street_num,
        'billing_street_name': billing_street_name,
        'billing_unit_number': billing_unit_number,
        'billing_city': billing_city,
        'billing_state': billing_state,
        'billing_zipcode': billing_zipcode
    }

    Database.execute_query(sql_insert, params)
    return True, "Customer registered successfully."


def check_user_credentials(email, password):
    """
    Checks user credentials for login.

    :param email: The email of the user trying to log in
    :param password: The plain-text password provided for login
    :return: True if credentials are valid, False otherwise
    """
    sql = text("SELECT cpassword FROM customer WHERE email = :email")
    result = Database.execute_query(sql, {'email': email}).fetchone()
    print(result)
    print(password)
    if result:
        hashed_password = result[0]
        print("Hashed password from DB:", hashed_password)  # 调试打印
        print("Plain text password:", password)  # 调试打印
        print("HASH password",generate_password_hash(password, method='pbkdf2:sha256'))
        password_check = check_password_hash(hashed_password, password)
        print("Password check result:", password_check)  # 调试打印
        return password_check
    return False
