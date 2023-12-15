from ..db.database import Database
from sqlalchemy import text
from datetime import datetime


def get_energy_by_customer_per_day(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT 
        DS.date, 
        COALESCE(SUM(DE.event_number), 0) as total_energy
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
    LEFT JOIN customer C on C.customer_id = L.customer_id
    WHERE (C.customer_id = :customer_id OR C.customer_id IS NULL)
    GROUP BY DS.date
    ORDER BY DS.date ASC
    """

    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    energy = []

    if results:
        for res in results:
            energy.append({"date": res[0], "energy": res[1]})
        return energy
    else:
        return None


def get_energy_by_customer_per_month(customer_id: int, start: datetime, end: datetime):
    sql_string = "SELECT YEAR(DE.event_datetime) AS year, MONTH(DE.event_datetime) AS month, SUM(event_number) as total_energy FROM "
    sql_string += (
        "device_event DE JOIN device_registered DR ON DE.device_id = DR.device_id"
    )
    sql_string += " JOIN location L ON L.location_id = DR.location_id"
    sql_string += " JOIN customer C on C.customer_id = L.customer_id"
    sql_string += " WHERE C.customer_id = :customer_id"
    sql_string += " AND DE.event_datetime BETWEEN :start AND :end"
    sql_string += " GROUP BY YEAR(DE.event_datetime), MONTH(DE.event_datetime) ORDER BY year, month ASC"

    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    energy = []

    if results:
        for res in results:
            energy.append({"year": res[0], "month": res[1], "energy": res[2]})
        return energy
    else:
        return None
