from ..db.database import Database
from sqlalchemy import text
from datetime import datetime


def get_price_of_locations(customer_id, start, end):

    str_sql = """
    SELECT l.location_id, ROUND(SUM(ep.price * de.event_number),4) AS energy_cost,
    CONCAT(l.location_unit_number,' ',l.location_street_num, ' ', l.location_street_name) AS address
    FROM device_event de
    JOIN device_registered dr ON de.device_id = dr.device_id
    JOIN location l ON dr.location_id = l.location_id
    JOIN energy_price ep ON ep.zipcode = l.location_zipcode AND ep.hour_of_day = HOUR(de.event_datetime)
    WHERE l.customer_id = :customer_id AND de.event_datetime BETWEEN :start AND :end AND de.event_label = 'EnergyReport'
    GROUP BY l.location_id
    """

    params = {"customer_id": customer_id, "start": start, "end": end}
    results = Database.execute_query(text(str_sql), params=params).fetchall()
    energy = []
    if results:
        for res in results:
            energy.append({"location_id": res[0], "address": res[2], "cost": res[1]})
        return energy
    else:
        return None



def get_price_of_each_device_type(customer_id, start, end):

    str_sql = """
    SELECT dm.model_type, ROUND(SUM(ep.price * de.event_number),4)
    FROM device_event de
    JOIN device_registered dr ON de.device_id = dr.device_id
    JOIN device_model dm ON dr.model_id = dm.model_id
    JOIN location l ON dr.location_id = l.location_id
    JOIN energy_price ep ON ep.zipcode = l.location_zipcode AND ep.hour_of_day = HOUR(de.event_datetime)
    WHERE l.customer_id = :customer_id AND de.event_datetime BETWEEN :start AND :end AND de.event_label = 'EnergyReport'
    GROUP BY dm.model_type
    """

    params = {"customer_id": customer_id, "start": start, "end": end}
    results = Database.execute_query(text(str_sql), params=params).fetchall()
    energy = []
    print(results)
    if results:
        for res in results:
            energy.append({"model_type": res[0], "price": res[1]})
        return energy
    else:
        return None