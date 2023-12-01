import mysql.connector
import os


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


if __name__ == "__main__":
    files = [
        "customer_gen.sql",
        "location_gen.sql",
        "device_model_gen.sql",
        "device_registered_gen.sql",
        "event_gen/test.sql",
        "price_gen/price_gen.sql",
    ]
    conn = get_conn()
    cursor = conn.cursor()
    for f in files:
        fp = open(f, "r")
        sql = fp.read()
        cursor.execute(sql)
        fp.close()
    close_conn(conn)
