from ..db.database import Database
from sqlalchemy import text
from datetime import datetime


def get_energy_by_customer_per_day(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT 
        DS.date, 
        COALESCE(ROUND(SUM(DE.event_number),3), 0) as total_energy
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


def get_customer_energy_per_locatoin(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT 
        ALL_L.location_id,
        DS.date, 
        COALESCE(ROUND(SUM(DE.event_number),4), 0) as total_energy
    FROM (
        SELECT ADDDATE(:start, t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) date
        FROM 
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t3,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t4
        WHERE ADDDATE(:start, t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) BETWEEN :start AND :end
    ) DS
    JOIN (
        SELECT L.location_id as location_id
        FROM
            location L JOIN customer CC ON L.customer_id = CC.customer_id
        WHERE
            CC.customer_id = :customer_id
    ) ALL_L
    LEFT JOIN device_registered DR ON DR.location_id = ALL_L.location_id
    LEFT JOIN device_event DE ON DATE(DE.event_datetime) = DS.date AND DE.device_id = DR.device_id
    GROUP BY ALL_L.location_id, DS.date
    ORDER BY ALL_L.location_id, DS.date ASC
    """
    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    energy = []
    last_location = -1
    idx = -1

    if results:
        for res in results:
            if not res[0] == last_location:
                idx += 1
                energy.append({"location_id": res[0], "energy": []})
                last_location = res[0]
            energy[idx]["energy"].append({"date": res[1], "energy": res[2]})
        return energy
    else:
        return None


def get_energy_by_customer_per_month(customer_id: int, start: datetime, end: datetime):
    sql_string = "SELECT YEAR(DE.event_datetime) AS year, MONTH(DE.event_datetime) AS month, ROUND(SUM(event_number),3) as total_energy FROM "
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


def get_energy_by_device_type(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT
    dm.model_type,
    ROUND(SUM(event_number),4) AS average_energy_consumption
    FROM device_event de
    JOIN device_registered dr ON de.device_id = dr.device_id
    JOIN device_model dm ON dr.model_id = dm.model_id
    JOIN location l ON dr.location_id = l.location_id
    WHERE l.customer_id = :customer_id AND de.event_datetime BETWEEN :start AND :end AND de.event_label = 'EnergyReport'
GROUP BY
    dm.model_type;
    """
    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    # convert results to a list of dictionaries
    energy = []
    if results:
        for res in results:
            energy.append({"device_type": res[0], "energy": res[1]})
        return energy


def get_energy_by_location_device_type(
    location_id: int, start: datetime, end: datetime
):
    sql_string = """
    SELECT
    dm.model_type,
    ROUND(SUM(event_number),4) AS average_energy_consumption
    FROM device_event de
    JOIN device_registered dr ON de.device_id = dr.device_id
    JOIN device_model dm ON dr.model_id = dm.model_id
    JOIN location l ON dr.location_id = l.location_id
    WHERE l.location_id = :location_id AND de.event_datetime BETWEEN :start AND :end AND de.event_label = 'EnergyReport'
GROUP BY
    dm.model_type;
    """
    params = {"location_id": location_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    # convert results to a list of dictionaries
    energy = []
    if results:
        for res in results:
            energy.append({"device_type": res[0], "energy": res[1]})
        return energy
    else:
        return [{"device_type": "No Energy Usage", "energy": 0}]


def get_energy_by_location_id(customer_id: int, start: datetime, end: datetime):
    sql_string = """
    SELECT l.location_id, ROUND(SUM(event_number),4) AS energy_cost,
    CONCAT(l.location_unit_number,' ',l.location_street_num, ' ', l.location_street_name) AS address
    FROM device_event de
    JOIN device_registered dr ON de.device_id = dr.device_id
    JOIN location l ON dr.location_id = l.location_id
    WHERE l.customer_id = :customer_id AND de.event_datetime BETWEEN :start AND :end AND de.event_label = 'EnergyReport'
    GROUP BY l.location_id
    """
    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    # convert results to a list of dictionaries
    energy = []
    if results:
        for res in results:
            energy.append({"location_id": res[0], "energy": res[1], "address": res[2]})
        return energy
    else:
        return None


def get_energy_of_all_devices(customer_id, start, end):
    sql_string = """
        SELECT
        dr.device_id,
        dm.model_name,
        dm.model_type,
        CONCAT(l.location_unit_number,' ',l.location_street_num, ' ', l.location_street_name) AS address,
        COALESCE(ROUND( SUM(total_energy_consumption),4),0) AS average_energy_consumption
    FROM
        (
            SELECT
                device_id,
                SUM(event_number) AS total_energy_consumption
            FROM
                device_event
            WHERE
                event_label = 'EnergyReport'
                AND event_datetime >= :start
                AND event_datetime < :end
            GROUP BY
                device_id
            HAVING
                SUM(event_number) IS NOT NULL # only consider devices that have on at least once
        ) AS subquery
        RIGHT JOIN device_registered dr ON subquery.device_id = dr.device_id
        JOIN device_model dm ON dr.model_id = dm.model_id
        JOIN location l ON dr.location_id = l.location_id
        WHERE l.customer_id = :customer_id
        GROUP BY dr.device_id
    """
    params = {"customer_id": customer_id, "start": start, "end": end}

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    # convert results to a list of dictionaries
    energy = []
    for result in results:
        energy.append(
            {
                "device_id": result[0],
                "model_name": result[1],
                "model_type": result[2],
                "address": result[3],
                "average_energy_consumption": result[4],
            }
        )

    return energy


def get_energy_of_all_device_per_day(
    customer_id: int, device_id: int, start: datetime, end: datetime
):
    sql_string = """
    SELECT 
        DS.date, 
        ROUND(COALESCE(SUM(DE.event_number), 0),4) as total_energy
    FROM (
        SELECT ADDDATE(:start, t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) date
        FROM 
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t1,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t2,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t3,
            (SELECT 0 i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) t4
        WHERE ADDDATE(:start, t4.i*1000 + t3.i*100 + t2.i*10 + t1.i) BETWEEN :start AND :end
    ) DS
    LEFT JOIN (
    SELECT * FROM device_event WHERE device_id = :device_id
    ) DE ON DATE(DE.event_datetime) = DS.date
    LEFT JOIN device_registered DR ON DE.device_id = DR.device_id
    LEFT JOIN location L ON L.location_id = DR.location_id
    LEFT JOIN customer C on C.customer_id = L.customer_id
    WHERE (C.customer_id = :customer_id OR C.customer_id IS NULL)
    GROUP BY DS.date
    ORDER BY DS.date ASC
    """

    params = {
        "customer_id": customer_id,
        "device_id": device_id,
        "start": start,
        "end": end,
    }

    results = Database.execute_query(text(sql_string), params=params).fetchall()

    energy = []

    if results:
        for res in results:
            energy.append({"date": res[0], "energy": res[1]})
        return energy
    else:
        return None
