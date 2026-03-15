'''General configuration settings for the database application.
Settings can be modified here to suit different environments or requirements.'''

#Class names
CLASS = ["Base", "Data"]

# Database
DEFAULT_DATABASE_NAME = 'standart.db'
DATABASE_PATH = "./data/" 
LOG_PATH = "./data/log.json"

# Column
COLUMN_TYPES = ["TEXT", "REAL", "INTEGER", "NULL", "DATE"]
ASCENDING = True
ORDER_BY_INDEX = "0"

#print colours -- > this will be further detailed in v2
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


