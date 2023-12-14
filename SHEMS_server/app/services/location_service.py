from ..db.database import Database
from sqlalchemy import text
from ..services.customer_service import get_customer_id


def get_customer_location(email):
    customer_id = get_customer_id(email)
    sql = text(
        "SELECT * FROM location WHERE customer_id = :customer_id AND in_use = true"
    )
    results = Database.execute_query(sql, {"customer_id": customer_id}).fetchall()
    # Mapping result to a array with column names as keys
    # print(results)
    res = []
    if results:
        for result in results:
            res.append(
                {
                    "location_id": result[0],
                    "customer_id": result[1],
                    "location_street_num": result[2],
                    "location_street_name": result[3],
                    "location_unit_number": result[4],
                    "location_city": result[5],
                    "location_state": result[6],
                    "location_zipcode": result[7],
                    "square_feet": result[8],
                    "num_bedrooms": result[9],
                    "num_occupants": result[10],
                    "start_date": result[11],
                }
            )
    else:
        res = []
    return res


def add_location(data):
    customer_id = get_customer_id(data.get("email"))
    start_date = "2022-07-31 23:59:59"

    sql_string = text(
        """
    INSERT INTO location (
        customer_id, 
        location_street_num, 
        location_street_name, 
        location_unit_number, 
        location_city, 
        location_state, 
        location_zipcode, 
        square_feet, 
        num_bedrooms, 
        num_occupants, 
        start_date
    ) VALUES (
        :customer_id, 
        :location_street_num, 
        :location_street_name, 
        :location_unit_number, 
        :location_city, 
        :location_state, 
        :location_zipcode, 
        :square_feet, 
        :num_bedrooms, 
        :num_occupants, 
        :start_date
    )
    """
    )

    params = {
        "customer_id": customer_id,
        "location_street_num": data.get("location_street_num"),
        "location_street_name": data.get("location_street_name"),
        "location_unit_number": data.get("location_unit_number"),
        "location_city": data.get("location_city"),
        "location_state": data.get("location_state"),
        "location_zipcode": data.get("location_zip_code"),
        "square_feet": data.get("square_feet"),
        "num_bedrooms": data.get("num_bedrooms"),
        "num_occupants": data.get("num_occupants"),
        "start_date": start_date,
    }

    success = Database.handle_transaction([{"query": sql_string, "params": params}])
    return success


def modify_location(location_id, num_bedrooms, num_occupants, square_feet):
    success = False
    first = True
    sql_string = "UPDATE location SET "
    if num_bedrooms is not None or square_feet is not None or num_occupants is not None:
        if num_bedrooms is not None:
            sql_string += "num_bedrooms = :num_bedrooms"
            first = False
        if num_occupants is not None:
            sql_string += (", " if not first else "") + "num_occupants = :num_occupants"
            first = False
        if square_feet is not None:
            sql_string += (", " if not first else "") + "square_feet = :square_feet"
        sql_string += " WHERE location_id = :location_id;"
        print(sql_string)
        sql = text(sql_string)
        params = {
            "location_id": location_id,
            "num_bedrooms": num_bedrooms,
            "num_occupants": num_occupants,
            "square_feet": square_feet,
        }
        success = Database.handle_transaction([{"query": sql, "params": params}])
    return success


def delete_location(location_id):
    sql1 = text(
        """
        UPDATE location SET in_use = false WHERE location_id = :location_id
        """
    )

    sql2 = text(
        """
        UPDATE device_registered SET in_use = false WHERE location_id = :location_id
        """
    )

    params = {"location_id": location_id}

    success = Database.handle_transaction(
        [{"query": sql1, "params": params}, {"query": sql2, "params": params}]
    )
    return success
