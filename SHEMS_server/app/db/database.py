import mysql.connector
from mysql.connector import Error
from config import Config

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                database='yourdb',
                user='youruser',
                password='yourpassword'
            )
        except Error as e:
            print(e)

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or ())
            return cursor
        except Error as e:
            print(e)
            self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()