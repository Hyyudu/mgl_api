import mysql.connector
from mysql.connector import errorcode

from config import DB_CONFIG

class DB:
    def __init__(self):
        try:
            cnx = mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cnx = cnx
            self.cursor = cnx.cursor(dictionary=True)

    def query(self, sql):
        self.cursor.execute(sql)
        return [row for row in self.cursor]

    def insert(self, table, data):
        pass
