import tkinter as tk

#define your functions here


#invoke Tk object
root = tk.Tk()
root.title("confidant v1")

#scaffold frames (draft)
#main frame
frame1=tk.Frame(master=root, width=640,height=480, bg="black")
#component frames
frame2=tk.Frame(master=frame1, width=400, height=240, bg="white")
frame3=tk.Frame(master=frame1, width=400, height=200, bg="white")
frame4=tk.Frame(master=frame1, width=200, height=240, bg="white")
frame5=tk.Frame(master=frame1, width=200, height=200, bg="white")


if __name__ == "__main__":
    frame1.pack(fill=tk.BOTH, expand=True)
    frame2.place(x=10,y=10)
    frame3.place(x=10,y=270,)
    frame4.place(x=430,y=10 )
    frame5.place(x=430, y=270)
    root.mainloop()
