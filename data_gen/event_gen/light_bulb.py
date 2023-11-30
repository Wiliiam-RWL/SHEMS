import mysql.connector
import datetime
import json
import random

EVENT_TYPE = []


def get_conn():
    try:
        conn = mysql.connector.connect(
            host="db-project.clt5dhnemxsz.us-east-2.rds.amazonaws.com",  # No 'https://' prefix
            user="admin",
            password="12345678",
            database="shems",
            port=3306,  # or your custom port
        )
        return conn

    # Database operations go here

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def close_conn(conn):
    if conn.is_connected:
        conn.close()


def get_light_bulb(conn):
    cursor = conn.cursor()
    cursor.execute(
        'SELECT device_id FROM device_model NATURAL JOIN device_registered WHERE model_type = "Light Bulb"'
    )
    light_bulb_ids = cursor.fetchall()
    lb_list = []
    for item in light_bulb_ids:
        item = list(item)
        lb_list += item
    return lb_list


def get_event_types(model_type: str, data: list):
    data = data["EventList"]

    def find_entry(model_type: str, data: list):
        for d in data:
            if d["model_type"] == model_type:
                return d

    events = find_entry(model_type=model_type, data=data)["events"]
    events += find_entry(model_type="General", data=data)["events"]
    return events


if __name__ == "__main__":
    # get all light bulb id
    conn = get_conn()
    lb_list = get_light_bulb(conn)
    close_conn(conn)

    # get all light bulb events
    fp = open("events.json")
    data = json.load(fp)
    events = get_event_types("Light Bulb", data)

    # randomly generate events
    start_date = datetime.datetime(
        year=2022, month=8, day=1, hour=0, minute=0, second=0
    )
    end_date = datetime.datetime(
        year=2022, month=9, day=30, hour=23, minute=59, second=59
    )

    print(start_date)
    print(end_date)
