from ..db.database import Database
from sqlalchemy import text
from ..services.customer_service import get_customer_id


def get_customer_location(email):
    customer_id = get_customer_id(email)
    sql = text("SELECT * FROM location WHERE customer_id = :customer_id")
    results = Database.execute_query(sql, {"customer_id": customer_id}).fetchall()
    # Mapping result to a array with column names as keys
    print(results)
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
