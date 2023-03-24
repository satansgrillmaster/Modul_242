import json
import sqlite3
from enums import QueryMethod


class DbManager:

    def __init__(self, db_path):
        self.db_path = db_path

    def execute_query(self, table_name, query_method, values, condition=None):

        if condition is None:
            condition = {}

        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        query = ""
        last_value_key = list(values)[-1]

        if query_method == QueryMethod.SELECT:
            query = "select "
            for x in values:
                query += x
                if list(values)[-1] != x:
                    query += ", "
            query += " from " + table_name
            if len(list(condition)) > 0:
                query += " where "
                for x, y in condition.items():
                    query += x + " = "
                    if isinstance(y,str):
                        query += "'" + y + "'"
                    else:
                        query += y
                    if list(condition)[-1] != x:
                        query += " and "

        elif query_method == QueryMethod.INSERT:
            query = 'insert into ' + table_name + " ("
            for x in values:
                query += x
                if list(values)[-1] != x:
                    query += ", "

            query += ") values ("
            for x, y in values.items():
                if isinstance(y, str):
                    query += "'" + y + "'"
                else:
                    query += y
                if x != last_value_key:
                    query += ", "
            query += ")"

        elif query_method == QueryMethod.UPDATE:
            query = 'update ' + table_name + " set "
            for x, y in values.items():
                if isinstance(y, str):
                    y = "'" + y + "'"
                query += x + " = " + y
                if list(values)[-1] != x:
                    query += ", "
            if len(list(condition)) > 0:
                query += " where "
                for x, y in condition.items():
                    if isinstance(y, str):
                        y = "'" + y + "'"
                    query += x + " = " + y
                    if list(condition)[-1] != x:
                        query += " and "

        elif query_method == QueryMethod.DELETE:
            query = "delete from " + table_name + " where "
            for x, y in condition.items():
                if isinstance(y, str):
                    y = "'" + y + "'"
                query += x + " = " + y
                if list(condition)[-1] != x:
                    query += " and "

        query += ";"
        print(query)
        res = cur.execute(query).fetchall()
        con.commit()
        con.close()
        return res