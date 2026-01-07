import sqlite3


class Data:

    def __init__(self,base):
        self.database = base if isinstance(base,str) else base.__dict__.get("name")
        self.connection = sqlite3.connect(self.database)

    def __repr__(self):
        return "Data operation tool for given database"

    def fetch(self, table, column, match):
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"SELECT {column} FROM {table} WHERE {column} = {match}").fetchall()

    
    def insert(self, table, *values):
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"INERT INTO {table} VALUES{values}").commit()

    def erase(self,table,column,data):
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {column}={data}").commit()

    def list(self, table, *column, order_by="0", ascending=True):
        order = column[int(order_by)]
        ascend = "ASC" if ascending else "DESC"
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"SELECT {','.join(column)} FROM {table} ORDER BY {order} {ascend}").fetchall()

    def list_all(self, table):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELCET * FROM {table}").fetchall()

