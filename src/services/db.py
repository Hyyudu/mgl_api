import pymysql


class DB:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='', db='magellan', charset='utf8')

    def query(self, sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        return [row for row in cursor]
