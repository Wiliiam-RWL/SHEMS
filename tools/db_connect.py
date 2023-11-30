import mysql.connector

try:
    conn = mysql.connector.connect(
        host="db-project.clt5dhnemxsz.us-east-2.rds.amazonaws.com",  # No 'https://' prefix
        user="admin",
        password="",
        database="shems",
        port=3306,  # or your custom port
    )
    if conn.is_connected():
        print("Connected to MySQL database")

    # Database operations go here

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    if conn.is_connected():
        conn.close()
        print("Connection closed.")
