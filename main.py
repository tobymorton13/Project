from tkinter import *
import mysql.connector
from datetime import datetime

now = datetime.now()  # variable containing current date and time

mydb = mysql.connector.connect(  # configure connection to mysql database
    host='localhost',
    user='root',
    password='password',
    port='3306',
    database='simplesrs')

mycursor = mydb.cursor()

mycursor.execute('SELECT SetName FROM sets')  # run select query on database
sets = mycursor.fetchall()  # assigns output of select query to set_data variable

gui = Tk()  # creates gui window
gui.title("SimpleSRS")  # gives the window a title
gui.geometry("1280x720")  # resizes window to 1280x720p

def fetch_sets():  # set selection menu
    # remove opening menu labels/buttons:
    logo_label.grid_forget()
    browse_button.grid_forget()
    set_select_header = Label(gui, text="Select a set below:", font=("Corbel", 30))  # creates header text label
    set_select_header.grid(column=0, row=0, padx="150")
    row_n = 1  # variable which will increment each set button's vertical position in window
    for item in sets:  # loop to display all sets output from extract statement above as buttons
        item = str(item)[2:-3]  #converts item from tuple to string and removes leading and trailing punctuation
        item.replace(" ", "")
        button = Button(gui, text=item, command=lambda chosen_set=item: set_options(chosen_set), font=("Corbel", 17), height=1, width=15)
        button.grid(column=0, row=row_n, padx="520", pady="5")
        row_n += 1

def set_options(chosen_set):  # management menu for chosen set, from here, lessons, reviews and edits to the set can be completed
    all_buttons = gui.grid_slaves()  #creates list of all buttons within the gui window
    for buttons in all_buttons:  #clears gui window
        buttons.destroy()
    set_options_header = Label(gui, text=chosen_set, font=("Corbel", 30))  #creates a header label, the title of the chosen set
    set_options_header.grid(column=0, row=0, padx="475")  #places the header label on the canvas
    set_manage_button = Button(set_window, text="Manage Set", command=set_management, font=("Corbel", 17), height=1, width=15)  #creates a "manage set" button
    set_manage_button.grid(column=0, row=1, padx="520", pady="5")  #places the manage set button on the canvas

def set_management():
    print("set management screen")
    all_buttons = gui.grid_slaves()  #creates list of all buttons within the gui window
    for buttons in all_buttons:  #clears gui window
        buttons.destroy()

# OPENING MENU:
logo = PhotoImage(file="logo.png")  # logo
logo_label = Label(image=logo)
logo_label.grid(column=0, row=0, padx="352", pady="50")

browse_text = StringVar()  # "browse sets" button
browse_text.set("Browse Sets")
browse_button = Button(gui, textvariable=browse_text, command=fetch_sets, font="Corbel", bg="#ffffff", height=3,
                       width=30)
browse_button.grid(column=0, row=1, padx="320")

gui.mainloop()  # runs the gui window
