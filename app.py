from setup import main, construct_class
import config
import datetime as dt
from time import sleep
from pathlib import Path
import json

print("=== Personal Confidant v1 ===")
name = input("your name : ")
print(f"Welcome {name.capitalize()}...")
sleep(1)
print("trying to find the latest setting...")
sleep(1)


#start the setup process and get the latest class instance based on the json data and the config file
try:
    db , data = main()
except ValueError:
    ask_setting = print(config.FAIL + "fatal : well..apparently there is no source to work with. Make sure you have a valid database file." + config.ENDC)
    #perhaps we can help user with some options here to create a new source or something, but for now let's just exit the application if there is no valid source to work with.
    sleep(0.5)
    print("leaving the application...")
    sleep(0.5)
    exit()


#start the main loop
while True:

    prompt_1 = input(
        """
_________________________________
please select the options below:

1. list available sources
2. work with a source
3. create new source
4. exit 

You :"""
        
        )

    match prompt_1:
        case "1":
            
            if len(db.table_index) == 0:
                print("\nThere is no available table. Building one would be a good idea.")
                sleep(1)
                ask_quit = input("Would you like to leave? (y/n) : ")
                if ask_quit.lower() == 'y':
                    print("leaving the applciation")
                    sleep(0.5)
                    break
                else:
                    print("returning to main menu...")
                    sleep(1)
            
            elif len(db.table_index) > 0:
                print(f"{len(db.table_index)} tables ready to build in database -> {db.name}")
                
                table_list = db.list_tables()
                
                for table_num, table_name in table_list.items():
                    print(f"{table_num} : {table_name}")
                    sleep(0.5)

            else:
                print("something awkward happened in the background, cannot execute the command now.")

        case "2":
            #first loop to select the source, second loop to work with the source
            while True:
                prompt_2 = input("""which source would like to work with ? : """)
                print(f"checking for {prompt_2} in database...")
                sleep(1)

                if prompt_2 not in db.table_index:
                    print("input is invalid, please give full source name or create one.")
                    sleep(1)
                    print("returning to main menu...")
                    sleep(1)
                    break
                
                #set the table
                working_table = prompt_2
                #bring columns for reference
                reference_columns = [column.get('col_name','') for column in db.registered_tables[working_table]]
                #this is the second loop
                while True:
                    prompt_3 = input("""
    _______________________
    select the operation
    1. fetch
    2. insert
    3. erase
    4. list
    5. list all
    6. return to main menu\n
    you : """)
                    
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
                                structured_result = zip(reference_columns, item)
                                for data in structured_result:
                                    print(f"{data[0]} : {data[1]}")
                                    sleep(0.5)
                        
                        case "2":
                            ask_type = input("""what would you like to do ?
                                            1. insert a value
                                            2. insert multiple values""")
                            
                            match ask_type:
                                case "1":
                                    for column in reference_columns:
                                        print(column)
                                    ask_column = input("which column ? : ")
                                    if ask_column not in reference_columns:
                                        print("column name is invalid, please try again.")
                                        continue
                                    ask_value = input("insert the value : ")

                                    data.insert(working_table,ask_column,ask_value)
                                    print(f"inserted the value {ask_value} into column {ask_column}")
                                    sleep(0.5)

                                case "2":
                                    ask_values = input("please insert the values in x y z form : ")
                                    ask_values = tuple([value.strip() for value in ask_values.split(' ')])
                                    
                                    if len(ask_values) != len(reference_columns):
                                        print("number of values do not match with the number of columns, please try again.")
                                    
                                    data.insert_multiple(working_table,*ask_values)
                                    print(f"inserted the values {ask_values} into columns {reference_columns}")
                                    sleep(0.5)
                                
                                case _:
                                    print("invalid input, please try again.")
                                    sleep(0.5)

                        case "3":
                            print(config.WARNING, "THIS IS A DANGER ZONE, BE CAREFUL. YOU CAN ERASE YOUR DATA(S) PERMANENTLY IF YOU MAKE A MISTAKE.", config.ENDC )

                            for column in reference_columns:
                                print(column)
                            
                            ask_column = input("which column ? : ")
                            ask_value = input("insert the value : ")

                            data.erase(working_table, ask_column, ask_value)
                            print("erased data")
                            sleep(0.5)

                        case "4":
                            for column in reference_columns:
                                print(column)

                            ask_column = input("which column(s) would you like to see (in x y z form) ? : ")
                            #prepare columns --> some validation techniques may be added in v2
                            columns = tuple([column.strip() for column in ask_column.split(' ')])

                            data.listing(working_table, *columns, order_by=config.ORDER_BY_INDEX, ascending=config.ASCENDING)
                            sleep(0.5)
                        
                        case "5":
                            consent = input("are yoru sure ?(y/n) : ")

                            if consent == "y":
                                #make this area pretty in v2, for now it just dumps everything in the terminal
                                data.list_all(working_table)
                            else:
                                print("operation cancelled, going back to main menu.")
                                sleep(0.5)
                        
                        case "6":
                            print("returning to main menu...")
                            sleep(0.5)
                            break
                            
        case "3":
            pass
            #will be v2 feature, to create new source with some basic settings. For now, you can create a source by registering a table and adding columns to it.

        case "4":
            print("leaving now .. ")
            sleep(1)
            print("goodbye !")
            sleep(0.5)
            exit()
