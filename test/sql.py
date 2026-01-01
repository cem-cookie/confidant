import sqlite3

class Database:
    '''Database class for managing SQLite database connections and operations.'''

    #set database configurations
    name = "standart"
    connected = False
    column_types = ["NULL", "INTEGER", "REAL", "TEXT", "BLOB"]
    registered_columns = []


    def create_connection(self):
        conn = sqlite3.connect(f"{self.name}.db")
        self.connected = True
        
        return conn
    
    
    #create table with given column specifics
    def create_table(self, table_name, columns = None):
        
        if self.connected is False:
            return "No database connection established."

        with self.create_connection() as conn:
            cursor = conn.cursor()
            if columns:
                response = cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)})').commit()
            else:
                response = cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(self.registered_columns)})').commit()
            
            return response
    


    def register_column(self, column_name, type, not_null= True, primary_key=False, unique = False, autoinc = False):
        
        if type.lower() not in [item.lower() for item in self.column_types]:
            return "invalid column type, you may define the columns: {', '.join(self.column_types)} "

        column_statement = f"{column_name} "
        
        if not_null:
            column_statement + "NOT NULL"
        
        if primary_key:
            column_statement + "PRIMARY KEY"
        
        if autoinc:
            column_statement + "AUTOINCREMENT"

        if unique:
            column_statement + "UNIQUE"        

        return column_statement