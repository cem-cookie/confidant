import sqlite3


class Data:
    "a mini object for data manipulation"

    def __init__(self,base):
        self.database = base if isinstance(base,str) else base.__class__.__dict__.get("path") 
        self.connection = sqlite3.connect(self.database) if ".db" in self.database else sqlite3.connect(f"{self.database}.db")
        

    def __str__(self):
        return f"Data operation tool for given database, currently connected to -> {self.database}"

    def fetch(self, table, column, match):
        with self.connection as conn:
            cursor= conn.cursor()
            result = cursor.execute(f"SELECT * FROM {table} WHERE {column} = {match}").fetchall()
            conn.close()

            return result

    def insert(self, table, column, value):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table}({column}) VALUES({value})")
            conn.close()

    def insert_multiple(self, table, *values):
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"INERT INTO {table} VALUES{values}")
            conn.close()


    def erase(self,table,column,data):
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {column}={data}")
            conn.close()

    def list(self, table, *column, order_by="0", ascending=True):
        #fetch specific columns
        order = column[int(order_by)]
        ascend = "ASC" if ascending else "DESC"
        
        #sql injection defences will be added in v2. 

        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"SELECT {','.join(column)} FROM {table} ORDER BY {order} {ascend}").fetchall()
            conn.close()

    def list_all(self, table):
        #fetch everything
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table}").fetchall()
            conn.close()
