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
            path = getattr(base, "path", "")
            name = getattr(base, "name", "")
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
    
    ######  BEWARE STARTING FROM THIS POINT!  ########
    #IMPORTANT : USE PARAMETIRED VALUES TO PREVENT SQL INJECTION AND SINGLE/DOUBLE QUOTE CHAOS
    
    def fetch(self, table, column, match):
        with self.connection as conn:
            cursor= conn.cursor()
            result = cursor.execute(f"SELECT * FROM {table} WHERE {column}=?", (match,)).fetchall()
            

        return result

    def insert(self, table, column, value):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table}({column}) VALUES(?)", (value,))
            

    def insert_multiple(self, table, *values):
        number_of_values = len(values)
        number_of_parameters = ["?"] * number_of_values
        with self.connection as conn:
            cursor= conn.cursor()
            cursor.execute(f"INSERT INTO {table} VALUES ({','.join(number_of_parameters)})", values) #no ned to put into tuple since *v returns tuple
            


    def erase(self,table,column,data):
        with self.connection as conn:
            cursor= conn.cursor()
            #this will delete entire row, consider more elegant solution for v2
            cursor.execute(f"DELETE FROM {table} WHERE {column}=?",(data,))
            

    def listing(self, table, *column, order_by="0", ascending=True):
        #fetch specific columns
        order = column[int(order_by)]
        ascend = "ASC" if ascending else "DESC"
        
        #sql injection defences will be added in v2. 

        with self.connection as conn:
            cursor= conn.cursor()
            result = cursor.execute(f"SELECT {','.join(column)} FROM {table} ORDER BY {order} {ascend}").fetchall()
        
        return result

    def list_all(self, table):
        #fetch everything
        with self.connection as conn:
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT * FROM {table}").fetchall()
            
        return result
        