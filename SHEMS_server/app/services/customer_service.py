from ..db.database import Database
from sqlalchemy import text


def get_user_info(email):
    """
    Gets the customer's information from the database.

    :param email: Customer's email
    :return: Customer's information
    """
    sql = text("SELECT * FROM customer WHERE email = :email")
    result = Database.execute_query(sql, {'email': email}).fetchone()
    # Mapping the result to a dictionary with column names as keys
    if result:
        customer_info = {
            "customer_id": result[0],
            "first_name": result[1],
            "last_name": result[2],
            "email": result[3],
            "billing_street_num": result[4],
            "billing_street_name": result[5],
            "billing_unit_number": result[6],
            "billing_city": result[7],
            "billing_state": result[8],
            "billing_zipcode": result[9],
        }
    else:
        customer_info = {}
    return customer_info


def get_customer_id(email):
    sql = text("SELECT customer_id FROM customer WHERE email = :email")
    result = Database.execute_query(sql, {'email': email}).fetchone()
    # return customer_id
    return result[0]
