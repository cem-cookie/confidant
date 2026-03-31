import sqlite3
import json
from pathlib import Path
import datetime as dt
from time import sleep
import config

#get config information and the base and data classes for setup
from src.base import Base
from src.data import Data

#get lates data from json
def process_json():
    "ensure that the log.json file exists and load the data for setup. Throw Exception if it does not exist"
    json_path = Path(config.LOG_PATH)

    if not json_path.exists() or json_path.stat().st_size == 0:
        with open(json_path, 'w') as f:
            json.dump([], f, indent=6)
        

    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if len(data) == 0:
        data.append({
            "class_name" : config.DEFAULT_CLASS_NAME,
            "name" : config.DEFAULT_DATABASE_NAME,
            "path" : config.DATABASE_PATH,
            "table_index" : [],
            "registered_tables" : {},
            "timestamp" : dt.datetime.timestamp(dt.datetime.now()),
            "created_at" : dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=6)

    #sort the data based on timestamp to ensure that the latest entry is at the end of the list.
    data.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    return data

def summon_class():
    "construct the class based on the data from the json file and the config file"
    data = process_json() #bring the json data
    latest_entry = data[0]  # get the latest entry based on the timestamp
    class_name = latest_entry.get('class_name', config.DEFAULT_CLASS_NAME)
    factory = type(class_name, (Base,), latest_entry)

    return factory()

def build(database: Base):
        
        if '.db' not in database.name:
            database.name += '.db'
        
        db_path = Path(config.DATABASE_PATH + database.name).expanduser()
        
        with sqlite3.connect(db_path) as con:
            try:        
                for table,columns in database.registered_tables.items():
                    sql_column = [f"{col['col_name']} {col['col_type']} { ' '.join(col['options']) }" for col in columns]  
                    con.execute(f"CREATE TABLE {table} ({', '.join(sql_column)})")
            
            #context manager will handle commit/rollback automatically
            except sqlite3.Error as e:
                print(f"An error occurred: {e}") 
            
            finally:
                pass
        
        if db_path.exists():
            return f"database [{database.name}] has been built successfully."



def main():
    """main function to run the setup process and create the class instance for app.py"""
    db = summon_class()
    build(db) # ensure that the database is built based on the latest settings from the json file and the config file. This will also update the log.json.
    data = Data(db)

    return db, data

