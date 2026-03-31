
from time import sleep

#mock database tables and data operations for app_test.py
db= ["table1", "table2", "table3"]  #mock database tables

#functions to mimic base_test.py functionalities
def list_tables():

        tables = enumerate(db)

        result = {table[0] : table[1] for table in tables}

        return result

print("=== Personal Confidant v1 ===")
name = input("Your name : ")
print(f"\n\nWelcome {name} !")
sleep(1)

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
            
            if len(db) == 0:
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
            
            elif len(db) > 0:
                print(f"{len(db)} tables ready to build in database -> mock_database")
                sleep(0.5) 
                
                table_list = list_tables()
                
                for table_num, table_name in table_list.items():
                    print(f"{table_num} : {table_name}")
                    sleep(0.5)

            else:
                print("something awkward happened in the background. Cannot satisfy the command now.")

        case "2":
            while True:
                prompt_2 = input("""which source would like to work with ? : """)
                print(f"checking for {prompt_2} in database...")
                sleep(1)

                if prompt_2 not in db:
                    print("input is invalid, please give full source name or create one.")
                    sleep(1)
                    print("returning to main menu...")
                    sleep(1)
                    break
                
                #set the table
                working_table = prompt_2
                #bring columns for reference

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
                        
                        print("fetched data")
                        sleep(0.5)
                        
                    
                    case "2":
                        ask_type = input("""what would you like to do ?
                                        1. insert a value
                                        2. insert multiple values""")
                        
                        match ask_type:
                            case "1":
                                print("inserted single value")
                                slpeep(0.5)

                            case "2":
                                print("inserted multiple values")
                                sleep(0.5)

                    case "3":
                        print("erased data")
                        sleep(0.5)

                    case "4":
                        print("listed data")
                        sleep(0.5)
                    
                    case "5":
                        print("listed all data")
                        sleep(0.5)
                    case "6":
                        print("returning to main menu...")
                        sleep(0.5)
                
                break 

        case "3":
            print("created new source")
            sleep(0.5)
        
        case "4":
            print("exiting program")
            sleep(0.5)
            break                    
