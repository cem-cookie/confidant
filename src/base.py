import sqlite3
from pathlib import Path
from config import DEFAULT_DATABASE_NAME, COLUMN_TYPES,DATABASE_PATH

class Base:
    '''Database class for managing SQLite database connections and operations.'''

    #set database configurations
    name = DEFAULT_DATABASE_NAME
    column_types = COLUMN_TYPES
    table_index = []
    registered_tables = {}

    #table registration
    def register_table(self, table_name):

        if table_name in self.table_index:
            return """table name already exists, please try another name or change the name of existing one. 
            (Hint:  this application is case naive, meaning that you can register a table with upper and lower case as same name.)""" 
        
        #register table name to index
        self.table_index.append(table_name)
        
        #update registered tables accordingly
        self.registered_tables.update({ 
            table_name : []
        })

        return f"table [{str(table_name)}] has been registered"
    

    #register column types with qulities for table
    def register_column(self, table_name, column_name,column_type, not_null= True, primary_key=False, autoinc = False, unique = False):

        if table_name not in self.table_index:
            return "table is not found in index, please register the table first before adding columns"
        
        if column_type.upper() not in self.column_types:
            return f"invalid column type, you may define the columns: {', '.join(self.column_types)}"

        column_register = {
            'col_name' : column_name,
            'col_type' : column_type,
            'options' : [],
        }

        if not_null:
            column_register['options'].append("NOT NULL")
        
        if primary_key:
            column_register['options'].append("PRIMARY KEY")
        
        if autoinc:
            column_register['options'].append("AUTOINCREMENT")

        if unique:
            column_register['options'].append("UNIQUE")

        
        #add column specs to table columns section
        return self.registered_tables[table_name].append(column_register)

    
    #list available tables
    def list_tables(self):

        tables = enumerate(self.table_index)

        result = {table[0] : table[1] for table in tables}

        return result

    
    def delete_table(self, table_name):

        if table_name not in self.table_index:
            return f"{table_name} does not seem to be in the index, please make sure table exists"
        
        try:
            self.registered_tables.pop(table_name)
            self.table_index.remove(table_name)

            return f"table [{table_name}] has been deleted successfully"
        except Exception as e:
            return f"an error occurred while deleting the table: {e}"
    
    def build(self):
        
        if '.db' not in self.name:
            self.name += '.db'
        
        path = Path(DATABASE_PATH + self.name).resolve()
        
        with sqlite3.connect(path) as con:
            try:        
                for table,columns in self.registered_tables.items():
                    sql_column = [f"{col['col_name']} {col['col_type']} {" ".join(col['options'])}" for col in columns]  
                    con.execute(f"CREATE TABLE {table} ({', '.join(sql_column)})")
            
            #context manager will handle commit/rollback automatically
            except sqlite3.Error as e:
                print(f"An error occurred: {e}") 
            
            finally:
                con.close()


            