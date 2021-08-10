from tkinter import *
import mysql.connector

#configure connection to mysql database:
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='tobias02',
    port='3306',
    database='simple srs'
)

mycursor = mydb.cursor()

mycursor.execute('SELECT SetID, SetName FROM sets')#run select query on database
sets = mycursor.fetchall()#assigns output of select query to set_data variable
for set in sets:
    print(set)

gui = Tk()#creates gui window
gui.title("SimpleSRS")#gives the window a title
gui.geometry("1280x720")

#set selection menu:
def fetch_sets():
    print("test")
    logo_label.grid_forget()
    browse_button.grid_forget()

#OPENING MENU:
#logo:
logo = PhotoImage(file="logo.png")
logo_label = Label(image=logo)
logo_label.grid(column=0, row=0, padx="352", pady="50")

#"browse sets" button:
browse_text = StringVar()
browse_button = Button(gui, textvariable=browse_text, command=fetch_sets, font="Corbel", bg="#ffffff", height=3, width=30)
browse_text.set("Browse Sets")
browse_button.grid(column=0, row=1, padx="320")

gui.mainloop()#runs the gui window
