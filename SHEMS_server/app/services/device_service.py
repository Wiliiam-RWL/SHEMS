from datetime import datetime
from ..db.database import Database
from sqlalchemy import text
from ..services.customer_service import get_customer_id


def get_customer_device(email):
    customer_id = get_customer_id(email)
    sql = text(
        "SELECT dr.device_id, dr.location_id, dr.model_id, dr.tag, dm.model_name, dm.model_type, "
        "l.location_street_num, l.location_state, l.location_street_name, l.location_unit_number, "
        "l.location_city, l.location_zipcode, dr.in_use "
        "FROM device_registered dr "
        "JOIN device_model dm ON dr.model_id = dm.model_id "
        "JOIN location l ON dr.location_id = l.location_id "
        "WHERE customer_id = :customer_id"
    )
    results = Database.execute_query(sql, {"customer_id": customer_id}).fetchall()
    res = []
    if results:
        print(results)
        for result in results:
            res.append(
                {
                    "device_id": result[0],
                    "location_id": result[1],
                    "model_id": result[2],
                    "tag": result[3],
                    "model_name": result[4],
                    "model_type": result[5],
                    "location_street_num": result[6],
                    "location_state": result[7],
                    "location_street_name": result[8],
                    "location_unit_number": result[9],
                    "location_city": result[10],
                    "location_zipcode": result[11],
                    "in_use": result[12],
                }
            )
    return res


def add_device(location_id, model_id, tag):
    sql_string = "INSERT INTO device_registered (location_id, model_id, tag) VALUES (:location_id, :model_id, :tag)"
    sql = text(sql_string)
    params = {"location_id": location_id, "model_id": model_id, "tag": tag}
    success = Database.handle_transaction([{"query": sql, "params": params}])
    return success


def delete_device(device_id):
    sql = text(
        "UPDATE device_registered SET in_use = false WHERE device_id = :device_id"
    )
    params = {"device_id": device_id}
    success = Database.handle_transaction([{"query": sql, "params": params}])
    return success


def update_device(device_id, tag):
    sql_string = "UPDATE device_registered SET tag = :tag WHERE device_id = :device_id"
    sql = text(sql_string)
    params = {"tag": tag, "device_id": device_id}
    success = Database.handle_transaction([{"query": sql, "params": params}])
    return success


def get_all_device_model():
    sql = text("SELECT * FROM device_model")
    results = Database.execute_query(sql).fetchall()
    res = []
    if results:
        for result in results:
            res.append(
                {
                    "model_id": result[0],
                    "model_type": result[1],
                    "model_name": result[2],
                }
            )
    else:
        res = []
    return res


def get_event_by_device_id(device_id: int, date: datetime):
    sql_string = """
    SELECT TIME(event_datetime), event_label, event_number
    FROM 
        device_event DE
    WHERE
        DE.device_id = :device_id AND
        DATE(DE.event_datetime) = DATE(:date)
    """
    params = {"device_id": device_id, "date": date}
    result = Database.execute_query(text(sql_string), params).fetchall()
    events = []
    idx = -1
    last_time = ""
    if result:
        for res in result:
            time = str(res[0])
            if not time == last_time:
                idx += 1
                events.append({})
                events[idx]["time"] = time
                last_time = time
            if res[2] is not None:
                events[idx][res[1]] = res[2]
            else:
                activity = events[idx].get("Activity", "")
                activity += (", " if len(activity) > 0 else "") + res[1]
                events[idx]["Activity"] = activity
        return events
    else:
        return [{"time": "all", "EnergyReport": 0}]
