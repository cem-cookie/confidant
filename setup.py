import json
from pathlib import Path

import config
#get config information and the base and data classes for setup
from src.base import Base
from src.data import Data

#get lates data from json
def process_json():
    "ensure that the log.json file exists and load the data for setup. Throw Exception if it does not exist"
    json_path = Path(config.LOG_PATH)

    if not json_path.exists():
        raise FileNotFoundError(f"Log file not found at {config.LOG_PATH}. Please ensure the file exists and try again.")
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    #sort the data based on timestamp to ensure that the latest entry is at the end of the list.
    data.sort(key=lambda x: x.get('timestamp', 0))
    return data


def construct_class(cls, **settings):
    "factory function to create instances of classes based on the class name"
    if cls not in config.CLASS:
        raise ValueError(f"Class {cls} not found in factory. Try to add the class to the config file and try again.")

    #yield the class instance based on config.CLASS[cls] and the settings from the json file
    # turn this function into a generator that yields the class instance based on the settings from the json file and the config file. 
    # This way, we can ensure that the app is always working with the latest data and configurations without having to change the code in app.py.    
    factory = type(cls, (Base,), settings)
    class_instance = factory()

    return class_instance 


def summon_class():
    "construct the class based on the data from the json file and the config file"
    #bring the latest entry from json data
    data = process_json()
    latest_entry = max(data, key= lambda x : x.get('timestamp', 0)) 


    class_name = latest_entry.get('class_name', 'Base')

    latest_class = construct_class(class_name, **latest_entry)

    return latest_class


def main():
    """main function to run the setup process and create the class instance for app.py"""
    latest_class = summon_class()

    print(f"""
    class {latest_class.__class__.__name__} has been summoned successfully with the following settings:
    database name : {latest_class.name}
    database path : {latest_class.path}
    column types : {latest_class.column_types}
    table index : {latest_class.table_index}
    registered tables : {latest_class.registered_tables}
""")
    
    db = latest_class
    data = Data(db)

    return db, data

