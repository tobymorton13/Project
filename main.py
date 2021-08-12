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
for sets in sets:
    print(sets)

gui = Tk()  # creates gui window
gui.title("SimpleSRS")  # gives the window a title
gui.geometry("1280x720")  # resizes window to 1280x720p

def fetch_sets():  # set selection menu
    # remove opening menu labels/buttons:
    logo_label.grid_forget()
    browse_button.grid_forget()
    # create header text label:
    set_select_header = Label(gui, text="Select a set below:", font=("Corbel", 30))
    set_select_header.grid(column=0, row=0, padx=200)
    row_n = 1  # variable which will increment each set button's vertical position in window
    for item in sets:  # loop to display all sets output from extract statement above as buttons
        button = Button(gui, text=item, command=lambda x=item: func(x))
        button.grid(column=0, row=row_n)
        row_n += 1




# OPENING MENU:
# logo:
logo = PhotoImage(file="logo.png")
logo_label = Label(image=logo)
logo_label.grid(column=0, row=0, padx="352", pady="50")

# "browse sets" button:
browse_text = StringVar()
browse_text.set("Browse Sets")
browse_button = Button(gui, textvariable=browse_text, command=fetch_sets, font="Corbel", bg="#ffffff", height=3,
                       width=30)
browse_button.grid(column=0, row=1, padx="320")

gui.mainloop()  # runs the gui window
