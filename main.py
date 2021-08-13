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

def set_select():  # set selection menu
    gui.destroy()
    select_window = Tk()  # creates gui window
    select_window.title("SimpleSRS")  # gives the window a title
    select_window.geometry("1280x720")  # resizes window to 1280x720p
    set_select_header = Label(select_window, text="Select a set below:", font=("Corbel", 30))  # creates header text label
    set_select_header.grid(column=0, row=0, padx=150)
    row_n = 1  # variable which will increment each set button's vertical position in window
    for item in sets:  # loop to display all sets output from extract statement above as buttons
        item = str(item)[2:-3]  #converts item from tuple to string and removes leading and trailing punctuation
        sets_button = Button(select_window, text=item, command=lambda chosen_set=item: set_options(chosen_set), font=("Corbel", 17), height=1, width=15)
        sets_button.grid(column=0, row=row_n, padx="520", pady="5")
        row_n += 1
    select_window.mainloop()

def set_options(chosen_set):  # management menu for chosen set, from here, lessons, reviews and edits to the set can be completed
    set_window = Tk()
    set_window.title(chosen_set)  # titles the window to the title of the user's chosen set
    set_window.geometry("1280x720")  # resizes window to 1280x720p
    set_options_header = Label(set_window, text=chosen_set, font=("Corbel", 30))  #creates a header label, the title of the chosen set
    set_options_header.grid(column=0, row=0, padx="150")  #places the header label on the canvas
    n_lessons="2"
    n_reviews="3"
    set_manage_button = Button(set_window, text="Manage Set", font=("Corbel", 17), height=1, width=15)  #creates a "manage set" button
    set_manage_button.grid(column=0, row=1, padx="520", pady="5")  #places the manage set button on the canvas
    lessons_button_text = ("You have " + n_lessons + " lessons available")  #variable storing text of "lessons available" button
    lessons_button = Button(set_window, text=lessons_button_text, font=("Corbel", 17), height=5, width=25)  #creates a button displaying number of available lesson for a chosen set
    lessons_button.grid(column=0, row=2, padx="0", pady="5")  #places the "lessons available" button
    reviews_button_text = ("You have "+n_reviews+" reviews available")  #variable storing text of "reviews available" button
    reviews_button = Button(set_window, text=reviews_button_text, font=("Corbel", 17),  #creates a button displaying number of available lesson for a chosen set
                            height=5, width=25)
    reviews_button.grid(column=0, row=3, padx="0", pady="5") #places the "reviews available" button
    back_button = Button(set_window, text="back", command=return_to_select, font=("Corbel", 17),
                            # creates a button displaying number of available lesson for a chosen set
                            height=5, width=25)
    back_button.grid(column=0, row=3, padx="0", pady="5")  # places the "reviews available" button


# OPENING MENU:
logo = PhotoImage(file="logo.png")  # logo
logo_label = Label(image=logo)
logo_label.grid(column=0, row=0, padx="352", pady="50")

browse_text = StringVar()  # "browse sets" button
browse_text.set("Browse Sets")
browse_button = Button(gui, textvariable=browse_text, command=set_select, font="Corbel", bg="#ffffff", height=3,
                       width=30)
browse_button.grid(column=0, row=1, padx="320")

gui.mainloop()  # runs the gui window
