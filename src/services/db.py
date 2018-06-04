import re

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
            self.column_lists = {}

    def _query(self, sql, data, need_commit=False):
        try:
            self.cursor.execute(sql, {key: val for key, val in data.items() if not isinstance(val, (dict, list, tuple))})
            if need_commit:
                self.cnx.commit()
            return self.cursor
        except Exception as e:
            print(e)
            print(sql)
            print(data)
            return False

    def query(self, sql, data=None, need_commit=False):
        sql = re.sub(r':([\w\d_]+)', r'%(\1)s', sql)
        return self._query(sql, data or {}, need_commit)

    def fetchAll(self, sql, data=None):
        self.query(sql, data or {})
        return [item for item in self.cursor]

    def fetchRow(self, sql, data=None):
        self.query(sql, data or {})
        for item in self.cursor:
            return item

    def fetchDict(self, sql, data=None, key='', val=''):
        self.query(sql, data or {})
        return {item.get(key): item.get(val) for item in self.cursor}

    def fetchColumn(self, sql, data=None):
        self.query(sql, data or {})
        return [list(item.values())[0] for item in self.cursor]

    def fetchOne(self, sql, data=None):
        self.query(sql, data or {})
        for item in self.cursor:
            return list(item.values())[0]

    def get_column_list(self, table):
        """Получает список столбцов таблицы"""
        if self.column_lists.get(table) is None:
            self.query("show columns from " + table)
            self.column_lists[table] = [row['Field'] for row in self.cursor]
        return self.column_lists[table]

    def upsert(self, operation, table, data, where=''):
        column_list = self.get_column_list(table)
        insert_data = {key: val for key, val in data.items() if key in column_list}
        sql = "insert into" if operation == 'insert' else 'update'
        sql += " " + table + " set " + ", ".join([field + " = %(" + field + ")s" for field in insert_data.keys()])
        if where:
            sql += " where " + where
        self.query(sql, insert_data, need_commit=True)
        return self.cursor.lastrowid

    def insert_many(self, table, data):
        column_list = self.get_column_list(table)
        insert_data = [
            {key: val for key, val in item.items() if key in column_list}
            for item in data
        ]
        sql = "insert into " + table + " (" + ", ".join(column_list) + ") values "
        ins_data = {}
        sql_values = []
        for i, item in enumerate(insert_data):
            ins_data.update({key + str(i): val for key, val in item.items()})
            sql_values.append("(" + ", ".join([":" + key+str(i) for key in item]) + ")")
        sql += ", \n".join(sql_values)
        return self.query(sql, ins_data, need_commit=True)

    def update(self, table, data, where):
        return self.upsert('update', table, data, where)

    def insert(self, table, data):
        if isinstance(data, dict):
            return self.upsert('insert', table, data)
        else:
            return self.insert_many(table, data)
