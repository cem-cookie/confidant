import setup
import config
from time import sleep
from pathlib import Path

#in any instance of exception or exit, wrapup and buildup function should be triggered to prevent data loss.

print("=== Personal Confidant v1 ===")
name = input("your name : ")
print(f"Welcome {name.capitalize()}...")
sleep(1)
print("trying to find the latest setting...")
sleep(1)


#start the setup process and get the latest class instance based on the json data and the config file
try:
    db , data = setup.start()
except ValueError:
    ask_setting = print(config.FAIL + "FATAL : well..apparently there is no source to work with. Make sure you have a valid database file." + config.ENDC)
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

1. list available tables
2. work with a table
3. create new table
4. exit 

You : """
        
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
                elif ask_quit.lower() == 'n':
                    print("returning to main menu...")
                    sleep(0.5)
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
                    sleep(2)
            
            elif len(db.table_index) > 0:
                print(f"{len(db.table_index)} tables ready to build in database -> {db.name}\n","-"*10)
                
                table_list = db.list_tables()
                
                for table_num, table_name in table_list.items():
                    print(f"{table_num+1} --> {table_name}")
                    sleep(0.5)

            else:
                print("something awkward happened in the background, cannot execute the command now.")

        case "2":
            #first loop to select the source, second loop to work with the source
            while True:
                prompt_2 = input("""which table would like to work with ? : """)
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
                                for row in structured_result:
                                    print(f"{row[0]} : {row[1]}")
                                    sleep(0.5)
                        
                        case "2":
                            ask_type = input("""what would you like to do ?
                                            1. insert a value
                                            2. insert multiple values
                                            
                                            You : """)
                            
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
                                    ask_values = input("please insert the values in x,y,z form : ")
                                    ask_values = tuple([value.strip() for value in ask_values.split(',')])
                                    
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

                            ask_column = input("which column(s) would you like to see (in x,y,z form) ? : ")

                            #prepare columns --> some validation techniques may be added in v2
                            columns = tuple([column.strip() for column in ask_column.split(',')])

                            for row in data.listing(working_table, *columns, order_by=config.ORDER_BY_INDEX, ascending=config.ASCENDING):
                                print(row)
                            sleep(0.5)
                        
                        case "5":
                            consent = input("are yoru sure ?(y/n) : ")

                            if consent == "y":
                                #make this area pretty in v2, for now it just dumps everything in the terminal
                                for row in data.list_all(working_table):
                                    print(row)
                            else:
                                print("operation cancelled, going back to main menu.")
                                sleep(0.5)
                        
                        case "6":
                            print("returning to main menu...")
                            sleep(0.5)
                            break
                            
        case "3":
            ask_table_name = input("what is the name of the new table ? : ")
            if ask_table_name in db.table_index:
                print("a table with the same name already exists, try another name.")
                sleep(0.5)
                break
            db.register_table(ask_table_name) #register the table

            #column registering starts here
            ask_column_num = int(input("how many columns would you like to have ? : "))
           
            for i in range(ask_column_num):
                #add attempt mechanism with inner while loop
                ask_column_name = input(f"what is the name of column {i+1} ? : ")
                ask_column_type = input(f"what is the type of column {i+1} ? ").strip().upper()
                
                if ask_column_type not in config.COLUMN_TYPES:
                    print(f"invalid column type, valid types are {', '.join(config.COLUMN_TYPES)}.")
                    sleep(0.5)
                    #for now give two chances, if a valid type cannot be given just assume that user(me) is a dummy and rollback to sqlite affinity guess
                    count_column_type_entry = 0
                    while count_column_type_entry <= 3:
                        
                        if count_column_type_entry == 3:
                            print("you pushed it too far now, try again later...")
                            sleep(0.5)
                            break
                        
                        ask_column_type_again = input("let's try again: ").strip().upper()
                        
                        if ask_column_type_again in config.COLUMN_TYPES:
                            count_column_type_entry = 0 
                            ask_column_type = ask_column_type_again
                            break
                        
                        count_column_type_entry += 1
                    
                    #check again if the column type is in predefined set or break the process flow if column type is not given properly
                if ask_column_type not in config.COLUMN_TYPES:
                    print("sorry but there is somethig wrong with your column definition...")
                    sleep(0.5)
                    print("")
                    print("cannot build the table.. returning to main menu")
                    sleep(0.5)
                    break
                ask_column_options = input(f"any options for column {i+1} ? (in x,y,z form) : ").upper().split(",")
                #small checkbox for column options
                options_checkbox = {o:False for o in config.VALID_COLUMN_OPTIONS}
                #validity check
                for option in ask_column_options:
                    option = option.strip()
                    if option not in config.VALID_COLUMN_OPTIONS:
                        print(f"invalid column option '{option}', valid options are {', '.join(config.VALID_COLUMN_OPTIONS)}.")
                        rectify = input("would you like to rectify the option ? (y/n) : ")
                        if rectify.lower() == 'y':
                            new_option = input("please enter the correct option : ")
                            if new_option.strip().upper() in config.VALID_COLUMN_OPTIONS:
                                ask_column_options[ask_column_options.index(option)] = new_option.strip().upper()
                                print("option rectified.")
                                sleep(0.5)
                        elif rectify.lower() == 'n':
                            print("skipping the option...")
                            ask_column_options.remove(option)
                            sleep(0.5)
                        else:
                            print("invalid column option, skipping the option...")
                            ask_column_options.remove(option)
                            sleep(0.5)
                    options_checkbox[option] = True
                       
                db.register_column(ask_table_name, ask_column_name, ask_column_type,
                                   not_null = options_checkbox["NOT NULL"],
                                   primary_key = options_checkbox["PRIMARY KEY"],
                                   autoinc = options_checkbox["AUTOINCREMENT"],
                                   unique = options_checkbox["UNIQUE"])
            #rebuild the database since its underlying structure altered
            #an exception handler here would be a wise move
            setup.build(db)

            print(f"table {ask_table_name} created successfully with given columns.")
            
        case "4":
            #that would be wise to put something in v2 to handle any exceptions
            print("checking if everything is saved correctly..")
            #put latest db information into log
            db.wrap_up() 
            #build up the latest tables of not built already in database
            setup.build(db)
            print("closing the connections and leaving now .. ")
            #some safe conenction clenaup will be here

            sleep(1)
            print(f"goodbye {name.capitalize()} !")
            sleep(0.5)
            exit()
