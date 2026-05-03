import tkinter as tk

#define the functions for the application here
def create_component(component_name, parent_frame, **kwargs):
    #build components and put them into dictionary for further access
    pass




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#--- GUI setup ---#
#invoke Tk object
root = tk.Tk()
root.title("confidant v1")

#scaffold frames (draft)
#main frame
main_frame=tk.Frame(master=root, width=640,height=480, bg="black")

#component frames
component_names = ["table_contents", "tables", "row_info", "settings"]



#table contents frame: shows the contents of the selected table
table_contents_frame=tk.Frame(master=main_frame, width=400, height=240, bg="white")


#tables frame: shows the list of tables in the database
tables_frame=tk.Frame(master=main_frame, width=400, height=200, bg="white")

#row info frame: shows the details of the selected row
row_info_frame=tk.Frame(master=main_frame, width=200, height=240, bg="white")

#settings frame: shows the settings and options for the application
settings_frame=tk.Frame(master=main_frame, width=200, height=200, bg="white")



if __name__ == "__main__":
    
    #pack the main frame
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    #place the component frames
    table_contents_frame.place(x=10,y=10)
    tables_frame.place(x=10,y=270,)
    row_info_frame.place(x=430,y=10 )
    settings_frame.place(x=430, y=270)
    
    #add widgets to the component frames here


    #start the main loop
    root.mainloop()
