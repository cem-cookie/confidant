from src.base import Base
from src.data import Data
import os
from pathlib import Path
from config import WARNING,ASCENDING,ORDER_BY_INDEX


db= Base()
data = Data(db)

#app will only work with setup.py
#setup.py will construct the class based on the latest entry in log.json and the config file, and then import the class to app.py for use. 
#This way, we can ensure that the app is always working with the latest data and configurations without having to change the code in app.py.


print("=== Personal Confidant v1 ===")
name = input("Your name : ")
prompt_1 = input(
    """
    Welcome {name} !

    please select the options below:

    1. list available sources
    2. work with a source
    3. create new source
    4. exit 
    
    """
    )

match prompt_1:
    case "1":
        
        if len(db.table_index) == 0:
            print("There is no available table. Building one would be a good idea.")
        
        elif len(db.table_index) > 0:
            print(f"{len(db.table_index)} tables ready to build in database -> {db.name}")
            
            table_list = db.list_tables()
            
            for table_num, table_name in table_list:
                print(f"{table_num} : {table_name}")

        else:
            print("something awkward happened in the background. Cannot satisfy the command now.")

    case "2":
        prompt_2 = input(f"""which source would like to work with ? : """)

        if prompt_2 not in db.table_index:
            print("input is invalid, please give full source name or create one.")
        
        #set the table
        working_table = prompt_2
        #bring columns for reference
        reference_columns = [column.get('col_name','') for column in db.registered_tables[working_table]]

        prompt_3 = input("""select the operation
                         1. fetch
                         2. insert
                         3. erase
                         4. list
                         5. list all """)
        
        match prompt_3:
            case "1":
                
                print("available columns:")
                for column in reference_columns:
                    print(column)
                
                ask_column = input("which column ? : ")
                ask_value = input("what are you looking for ? : ")

                results = data.fetch(working_table,ask_column,ask_value)

                print("here is the result(s):")
                for item in results:
                    structured_result = list(zip(reference_columns,data))
                    for data in structured_result:
                        print(f"data[0] : data[1]") 
            
            case "2":
                ask_type = input("""what would you like to do ?
                                 1. insert a value
                                 2. insert multiple values""")
                
                match ask_type:
                    case "1":
                        for column in reference_columns:
                            print(column)
                        ask_column = input("which column ? : ")
                        ask_value = input("insert the value : ")

                        data.insert(working_table,ask_column,ask_value)

                    case "2":
                        ask_values = input("please insert the values in x y z form : ")
                        ask_values = tuple([value.strip() for value in ask_values.split(' ')])
                        if len(ask_values) != len(reference_columns):
                            print("number of values do not match with the number of columns, please try again.")
                        
                        data.insert_multiple(working_table,*ask_values)

            case "3":
                print(WARNING, "THIS IS A DANGER ZONE, BE CAREFUL")

                for column in reference_columns:
                    print(column)
                
                ask_column = input("which column ? : ")
                ask_value = input("insert the value : ")

                data.erase(working_table, ask_column, ask_value)

            case "4":
                for column in reference_columns:
                    print(column)

                ask_column = input("which column(s) would you like to see (in x y z form) ? : ")
                #prepare columns --> some validation techniques may be added in v2
                columns = tuple([column.strip() for column in ask_column.split(' ')])

                data.list(working_table, *columns, order_by=ORDER_BY_INDEX, ascending=ASCENDING)
            
            case "5":
                consent = input("are yoru sure ?(y/n) : ")

                if consent == "y":
                    data.list_all(working_table)
                else:
                    print("operation cancelled, going back to main menu.")

    case "3":
        pass
        #will be v2 feature, to create new source with some basic settings. For now, you can create a source by registering a table and adding columns to it.

    case "4":
        print("goodbye !")
        exit()
