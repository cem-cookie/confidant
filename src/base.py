import sqlite3

class DataBase:
    '''Database class for managing SQLite database connections and operations.'''

    #set database configurations
    name = "standart"
    connected = False
    column_types = ["TEXT", "REAL", "INTEGER", "NULL", "DATE"]
    registered_columns = []


    def create_connection(self):
        if self.connected:
            return f"connection to {name}.db is already alive"
        
        connection = sqlite3.connect(f"{self.name}.db")
        #cursor = connection.cursor()
        self.connected = True
        
        return connection#,cursor
    
    #register column types with qulities for table
    def register_column(self, column_name, column_type, not_null= True, primary_key=False, autoinc = False, unique = False):
        
        if column_type.upper() not in [item for item in self.column_types]:
            return f"invalid column type, you may define the columns: {', '.join(self.column_types)}"

        date_exists = column_type.upper() is "DATE" 
        column_statement = f"{column_name.upper()} TEXT NOT NULL" if date_exists else f"{column_name.upper()} {column_type.upper()}"
        
        if not_null:
            column_statement += " NOT NULL"
        
        if primary_key:
            column_statement += " PRIMARY KEY"
        
        if autoinc:
            column_statement += " AUTOINCREMENT"

        if unique:
            column_statement += " UNIQUE"        

        self.register_column.append(column_statement)
    
    
    #create table with given column specifics
    def create_table(self, table_name, columns = None ):
        
        if self.connected is False:
            return "No database connection established."

        with self.create_connection() as conn:
            cursor = conn.cursor()
            if columns:
                response = cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(columns)})').commit()
            else:
                response = cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(self.registered_columns)})').commit()
            
        
        return response
    
    
    
    def purge_table(self, table_name):

        with self.create_connection() as conn:
            
            try:
                cursor= conn.cursor()
                response = cursor.execute(f"DROP TABLE IF EXISTS {table_name}").commit()
                
                return response
            
            except Exception as e:
                return f"Fatal Error during the operation : {e}"
            
    def disconnect(self):
        pass
