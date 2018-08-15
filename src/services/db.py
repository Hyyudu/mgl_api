import json
import re
import traceback
from collections import defaultdict
from datetime import datetime
from typing import Dict

import mysql.connector
import sys
from config import DB_CONFIG
from decimal import Decimal
from mysql.connector import errorcode


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
            self.last_sql = ""

    def _query(self, sql, data, need_commit=False):
        try:
            self.cursor.execute(sql,
                                {key: val for key, val in data.items() if not isinstance(val, (dict, list, tuple))})
            if need_commit:
                self.cnx.commit()
            self.last_sql = sql

            return self.cursor
        except Exception as e:
            error_text = "Error executing query: " + sql+"\n"+json.dumps(data, indent=4) +"\n" + "\n".join(traceback.format_stack())
            from src.services.misc import get_error_logger

            logger = get_error_logger(__name__)
            logger.error("======================================================================")
            logger.exception(error_text, exc_info=e)
            print(error_text)
            e.sql = sql
            raise e

    def query(self, sql, data=None, need_commit=False):
        sql = re.sub(r':([\w\d_]+)', r'%(\1)s', sql)
        return self._query(sql, data or {}, need_commit)

    def get_last_sql(self):
        return self.last_sql

    def get_result(self):
        for item in self.cursor:
            item = {
                key if type(key) != bytes else key.decode():
                    val if type(val) != datetime else val.strftime("%Y-%m-%d %H:%M:%S")
                for key, val in item.items()}
            yield item

    def fetchAll(self, sql, data=None, associate='', cumulative=False):
        self.query(sql, data or {})
        result = []
        for item in self.get_result():
            item = {key: float(val) if type(val) is Decimal else val for key, val in item.items()}
            result.append(item)
        self.cnx.commit()
        if associate:
            if not cumulative:
                result = {item[associate]: item for item in result}
            else:
                out = defaultdict(list)
                for item in result:
                    out[item[associate]].append(item)
                result = dict(out)
        return result


    def fetchRow(self, sql, data=None):
        self.query(sql, data or {})
        for item in self.get_result():
            self.cnx.commit()
            return item

    def fetchDict(self, sql, data=None, key='', val=''):
        self.query(sql, data or {})
        ret = {item.get(key): item.get(val) for item in self.get_result()}
        self.cnx.commit()
        return ret

    def fetchColumn(self, sql, data=None):
        self.query(sql, data or {})
        ret = [list(item.values())[0] for item in self.get_result()]
        self.cnx.commit()
        return ret

    def fetchOne(self, sql, data=None):
        self.query(sql, data or {})
        for item in self.get_result():
            self.cnx.commit()
            return list(item.values())[0]

    def get_column_list(self, table):
        """Получает список столбцов таблицы"""
        if self.column_lists.get(table) is None:
            self.query("show columns from " + table)
            self.column_lists[table] = [row['Field'] for row in self.get_result()]
        return self.column_lists[table]

    def upsert(self, operation, table, data, where='', on_duplicate_key_update=''):
        column_list = self.get_column_list(table)
        insert_data = {key: val for key, val in data.items() if key in column_list}
        sql = "insert into" if operation == 'insert' else 'update'
        sql += " " + table + " set " + ", ".join([field + " = %(" + field + ")s" for field in insert_data.keys()])
        if where:
            sql += " where " + where
        if on_duplicate_key_update:
            sql += " on duplicate key update " + on_duplicate_key_update
        self.query(sql, insert_data, need_commit=True)
        return self.cursor.lastrowid if operation == 'insert' else self.affected_rows()

    def insert_many(self, table, data, on_duplicate_key_update=''):
        column_list = self.get_column_list(table)
        insert_data = [
            {key: val for key, val in item.items() if key in column_list}
            for item in data
        ]
        sql = "insert into " + table + " (" + ", ".join(insert_data[0].keys()) + ") values "
        ins_data = {}
        sql_values = []
        for i, item in enumerate(insert_data):
            ins_data.update({key + str(i): val for key, val in item.items()})
            sql_values.append("(" + ", ".join([":" + key + str(i) for key in item]) + ")")
        sql += ", \n".join(sql_values)
        if on_duplicate_key_update:
            sql += " on duplicate key update " + on_duplicate_key_update
        return self.query(sql, ins_data, need_commit=True)

    def update(self, table, data, where):
        return self.upsert('update', table, data, where=where)

    def insert(self, table, data, on_duplicate_key_update=''):
        if isinstance(data, dict):
            return self.upsert('insert', table, data, on_duplicate_key_update=on_duplicate_key_update)
        else:
            return self.insert_many(table, data, on_duplicate_key_update=on_duplicate_key_update)

    def affected_rows(self):
        return self.cursor.rowcount

    @staticmethod
    def construct_where(params: Dict) -> str:
        where = []
        for key, val in params.items():
            if isinstance(val, (tuple, list, set)):
                where.append(key + " in (" + ", ".join([":" + key + "__" + str(i) for i in range(len(val))]) + ") ")
            else:
                where.append(key + " = :" + key)
        return " and ".join(where)

    @staticmethod
    def construct_params(params: Dict) -> Dict:
        new_params = {}
        for key, val in params.items():
            if isinstance(val, (tuple, list, set)):
                new_params.update({key + "__" + str(i): item for i, item in enumerate(val)})
            else:
                new_params[key] = val
        params = new_params
        return params
