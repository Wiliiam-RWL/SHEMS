from ..db.database import Database
from sqlalchemy import text
from ..services.customer_service import get_customer_id


def get_customer_device(email):
    customer_id = get_customer_id(email)
    sql = text("SELECT * FROM device_registered dr JOIN device_model dm ON dr.model_id = dm.model_id"
               " JOIN location l ON dr.location_id = l.location_id"
               " WHERE customer_id = :customer_id")
    results = Database.execute_query(sql, {'customer_id': customer_id}).fetchone()
    res = []
    if results:
        for result in results:
            print(res)
            res.append({
                "device_id": result[0],
                "location_id": result[1],
                "model_id": result[2],
                "tag": result[3],
                "model_name": result[5],
                "model_type": result[6],
                "location_name": result[8],
                "location_address": result[9],
                "location_latitude": result[10],
                "location_longitude": result[11],
                "location_description": result[12]
            })
    return res


def add_device(location_id, model_id, tag):
    sql = text("INSERT INTO device_registered (location_id, model_id, tag) VALUES (:location_id, :model_id, :tag)")
    Database.execute_query(sql, {'location_id': location_id, 'model_id': model_id, 'tag': tag})
    return True


def delete_device(device_id):
    sql = text("DELETE FROM device_registered WHERE device_id = :device_id")
    Database.execute_query(sql, {'device_id': device_id})
    return True


def get_all_device_model():
    sql = text("SELECT * FROM device_model")
    results = Database.execute_query(sql).fetchall()
    res = []
    if results:
        for result in results:
            res.append({
                "model_id": result[0],
                "model_type": result[1],
                "model_name": result[2],
            })
    else:
        res = []
    return res
