import json
#get config information from config.py
import config
from src.base import Base
from src.data import Data
from pathlib import Path



#get lates data from json
def process_json():
    "ensure that the log.json file exists and load the data for setup. Throw Exception if it does not exist"
    json_path = Path(config.LOG_PATH)

    if not json_path.exists():
        raise FileNotFoundError(f"Log file not found at {config.LOG_PATH}. Please ensure the file exists and try again.")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def construct_class(cls, **settings):
    "factory function to create instances of classes based on the class name"
    if cls not in config.CLASS:
        raise ValueError(f"Class {cls} not found in factory. Try to add the class to the config file and try again.")
    
    factory = type(cls, (Base,), settings)
    class_instance = factory()

    return class_instance 


def summon_class():
    "construct the class based on the data from the json file and the config file"
    #bring json data for setup
    data = process_json()

    #get latest entry from json data
    latest_entry = max(data, key= lambda x : x.get('timestamp', 0)) 

    
    class_name = latest_entry.get('class_name', 'Base')

    latest_class = construct_class(class_name, **latest_entry)

    return latest_class



