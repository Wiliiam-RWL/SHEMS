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


def get_price_by_customer_per_month(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT 
        YEAR(DE.event_datetime) AS year, 
        MONTH(DE.event_datetime) AS month, 
        ROUND(SUM(EP.price * DE.event_number),3) as total_price
    FROM 
        device_event DE 
        JOIN device_registered DR ON DE.device_id = DR.device_id
        JOIN location L ON L.location_id = DR.location_id
        JOIN customer C ON C.customer_id = L.customer_id
        JOIN energy_price EP ON ep.zipcode = l.location_zipcode AND ep.hour_of_day = HOUR(de.event_datetime)
    WHERE 
        C.customer_id = :customer_id
        AND DE.event_datetime BETWEEN :start AND :end
    GROUP BY 
        YEAR(DE.event_datetime), MONTH(DE.event_datetime) 
    ORDER BY 
        year, month ASC
    """

    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    energy = []

    if results:
        for res in results:
            energy.append({"year": res[0], "month": res[1], "price": res[2]})
        return energy
    else:
        return None




def get_price_by_customer_per_day(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT 
        DS.date, 
        COALESCE(ROUND(SUM(EP.price * DE.event_number), 3), 0) AS price
    FROM (
        SELECT ADDDATE(:start, t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) date
        FROM 
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t3,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t4
        WHERE ADDDATE(:start, t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) BETWEEN :start AND :end
    ) DS
    LEFT JOIN device_event DE ON DATE(DE.event_datetime) = DS.date
    LEFT JOIN device_registered DR ON DE.device_id = DR.device_id
    LEFT JOIN location L ON L.location_id = DR.location_id
    LEFT JOIN customer C ON C.customer_id = L.customer_id
    LEFT JOIN energy_price EP ON EP.zipcode = L.location_zipcode AND EP.hour_of_day = HOUR(DE.event_datetime)
    WHERE (C.customer_id = :customer_id OR C.customer_id IS NULL)
    GROUP BY DS.date
    ORDER BY DS.date ASC
    """

    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    energy = []

    if results:
        for res in results:
            energy.append({"date": res[0], "price": res[1]})
        return energy
    else:
        return None