import os
import mysql.connector
import datetime
import json
import random

EVENT_TYPE = []


def get_conn():
    fp = open("../../tools/connection.txt")
    user = fp.readline().replace("\n", "")
    pwd = fp.readline().replace("\n", "")
    print(user, pwd)
    try:
        conn = mysql.connector.connect(
            host="shems.clt5dhnemxsz.us-east-2.rds.amazonaws.com",  # No 'https://' prefix
            user=user,
            password=pwd,
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
        "SELECT device_id FROM device_model NATURAL JOIN device_registered WHERE device_id = 12 OR device_id = 14"
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


class LightBulb:
    def __init__(self, id: int, on_off: str, mode: str) -> None:
        self.id = id
        self.on_off = on_off
        self.mode = mode
        self.last_update = datetime.datetime(
            year=2022, month=8, day=1, hour=0, minute=0, second=0
        )
        self.kwh_min = 0.001

    def send_event(self, now: datetime.datetime):
        # this function is used to generated mock data
        if self.on_off == "Off":
            # randomly turn on and off to simulate user operations
            if random.randrange(0, 4000) == 0:
                self.on_off = "On"
                self.last_update = now
                return [{"event_label": "On", "number": None}]
            else:
                return []
        else:
            event_list = []

            if random.randrange(0, 50) == 0:
                # randomly turn off light
                self.on_off = "Off"
                event_list.append({"event_label": "Off", "number": None})
                energy = ((now - self.last_update).total_seconds() / 60) * self.kwh_min
                if self.mode == "BrightMode":
                    energy = energy * 1.5
                self.last_update = now
                event_list.append({"event_label": "EnergyReport", "number": energy})
            elif (now - self.last_update).total_seconds() >= 5 * 60:
                # check if there is need to update energy use
                energy = ((now - self.last_update).total_seconds() / 60) * self.kwh_min
                if self.mode == "BrightMode":
                    energy = energy * 1.5
                self.last_update = now
                event_list.append({"event_label": "EnergyReport", "number": energy})

            # randomly set different mode
            if random.randrange(0, 100) == 0:
                if self.mode == "BrightMode":
                    self.mode = "DarkMode"
                    event_list.append({"event_label": "DarkMode", "number": None})
                else:
                    self.mode = "BrightMode"
                    event_list.append({"event_label": "BrightMode", "number": None})
            return event_list


if __name__ == "__main__":
    # get all light bulb id
    conn = get_conn()
    lb_list = get_light_bulb(conn)
    close_conn(conn)

    # get all light bulb events
    fp = open("events.json")
    data = json.load(fp)
    fp.close()
    events = get_event_types("Light Bulb", data)

    # randomly generate events
    start_datetime = datetime.datetime(
        year=2022, month=8, day=1, hour=0, minute=0, second=0
    )
    now = start_datetime
    end_datetime = datetime.datetime(
        year=2022, month=12, day=31, hour=23, minute=59, second=59
    )

    bulbs = []
    fp = open("test.txt", "w")
    fp.write(
        "INSERT INTO device_event \n(device_id, event_datetime, event_label, event_number) VALUE \n"
    )
    sql = "({}, '{}', '{}', {}),\n"

    for lb in lb_list:
        bulb = LightBulb(lb, "Off", "BrightMode")
        bulbs.append(bulb)

    while now < end_datetime:
        now = now + datetime.timedelta(minutes=5)
        for b in bulbs:
            event_list = b.send_event(now)
            for e in event_list:
                fp.write(
                    sql.format(
                        b.id,
                        now,
                        e["event_label"],
                        "NULL" if e["number"] is None else e["number"],
                    )
                )
    fp.write(";")
    fp.close()
