import sqlite3
import os


class Data:
    """a mini object for data manipulation"""

    def __init__(self, base):
        """Initialize a Data helper for the given 'Base' instance."""
        if isinstance(base, str):
            # ``base`` is already a full path (may already include .db)
            db_path = base
        else:
            # Retrieve class attributes safely; fallback to config defaults if missing
            path = getattr(base.__class__, "path", "")
            name = getattr(base.__class__, "name", "")
            db_path = f"{path}{name}"

        # Ensure the path ends with .db
        if not db_path.lower().endswith('.db'):
            db_path = f"{db_path}.db"

        # Expand user (~) and create parent directory if needed
        db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.database = db_path
        self.connection = sqlite3.connect(self.database)
        

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

    def listing(self, table, *column, order_by="0", ascending=True):
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
