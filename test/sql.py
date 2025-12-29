import sqlite3

class Database:
    '''Database class for managing SQLite database connections and operations.'''

    #set database configurations
    name = "app.db"
    initial_tables = []
    connection = create_connection()


    def create_connection(self):
        try:
            conn = sqlite3.connect(self.name)
            self.connected = True
            return conn
        
        except sqlite3.Error as e:
            self.connected = False
            return f"Error connecting to database:\n___\n {e}"
            
    

    def create_table(self, table_name, columns=None):
        if self.connection is False:
            return "No database connection established."

        conn = self.connection
        cursor = conn.cursor()
        res = cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} ({columns})''').commit()
        
        return res
        
        
    def create_tables(self, tables):
        for table_name, columns in tables.items():
            self.create_table(table_name, columns)

    def set_data(self, table_name, data):
        pass

    def get_data(self, table_name, conditions=None):
        pass
    
    def update_data(self, table_name, updates, conditions=None):
        pass

    def delete_data(self, table_name, conditions=None):
        pass

