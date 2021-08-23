from tkinter import *
import mysql.connector
from datetime import datetime, timedelta
import time

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


def clear_window():  # function used whenever a new page is loaded and all widgets from previous menu need to be cleared
    all_buttons = gui.grid_slaves()  # creates list of all buttons within the gui window
    for buttons in all_buttons:  # clears gui window
        buttons.destroy()


def fetch_sets():  # set selection menu
    # remove opening menu labels/buttons:
    logo_label.grid_forget()
    browse_button.grid_forget()
    set_select_header = Label(gui, text="Select a set below:", font=("Corbel", 30))  # creates header text label
    set_select_header.grid(column=0, row=0, padx="150")
    row_n = 1  # variable which will increment each set button's vertical position in window
    for item in sets:  # loop to display all sets output from extract statement above as buttons
        item = str(item)[2:-3]  # converts item from tuple to string and removes leading and trailing punctuation
        item.replace(" ", "")
        button = Button(gui, text=item, command=lambda chosen_set=item: set_options(chosen_set), font=("Corbel", 17),
                        height=1, width=15)
        button.grid(column=0, row=row_n, padx="520", pady="5")
        row_n += 1


def remove_punctuation(i):  # function to remove unwanted punctuation from a string
    i = str(i)
    disallowed_characters = "(),"  # creation of a set of unwanted punctuation
    for character in disallowed_characters:  # removes all unwanted puctuation from 'i' to allow it to be used it the sql select statement
        i = i.replace(character, "")


def set_options(chosen_set):  # chosen set option menu, from here, lessons, reviews and edits to set can be completed
    clear_window()
    global global_chosen_set  # creation of a global chosen_set variable to allow it to be used in the set management screen
    global_chosen_set = chosen_set
    set_options_header = Label(gui, text=chosen_set,
                               font=("Corbel", 30))  # creates a header label, the title of the chosen set
    set_options_header.grid(column=0, row=0, padx="475")  # places the header label on the canvas
    set_manage_button = Button(gui, text="Manage Set", command=set_management, font=("Corbel", 17), height=1,
                               width=15)  # creates a "manage set" button
    set_manage_button.grid(column=0, row=1, padx="520", pady="5")  # places the manage set button on the canvas
    # !!!!!CREATE QUERY TO EXTRACT SET ID FOR "CHOSEN SET", USE JOIN STATEMENTS TO EXTRACT ITEMID's and SRSPos and Last Review
    mycursor.execute('SELECT SetID, SetName FROM sets')  # sql statement to select all setid's and setnames
    set_list = mycursor.fetchall()  # assign output of sql statement to set_list variable
    tuple_in_list = [set_list for set_list in set_list if
                     chosen_set in set_list]  # outputs tuple within list that contains chosen_set
    chosen_setid = (str(tuple_in_list))[2]  # selects character of output tuple that correponds to chosen set's setid
    global global_chosen_setid  #  creation of a global chosen_setid variable to allow it to be used in the set management screen
    global_chosen_setid = chosen_setid
    mycursor.execute(
        'SELECT items.ItemID FROM Items INNER JOIN sets ON Items.SetID = sets.SetID WHERE sets.SetID = (%s)' % (
            chosen_setid))
    itemid_list = mycursor.fetchall()
    items_to_learn = []
    for i in itemid_list:  # loop to verify which items are due for a lesson or review
        i = str(i)  # convert each itemid from tuple to string
        disallowed_characters = "(),[]'"  # creation of a set of unwanted punctuation
        for character in disallowed_characters:  # removes all unwanted puctuation from 'i' to allow it to be used it the sql select statement
            i = i.replace(character, "")
        mycursor.execute('SELECT SRSPos FROM items WHERE ItemID = (%s)' % (
            i))  # sql statement to extract item i's position in the srs system
        i_srspos = mycursor.fetchall()  # assigns the srs pos of item i to a variable
        mycursor.execute('SELECT LastReview FROM items WHERE ItemID = (%s)' % (
            i))  # sql statement to extract datetime of item i's last review
        i_lastreview = mycursor.fetchall()  # assigns the datetime of item i's last review to a variable
        now = str(datetime.now())  #store current date time in a variable
        print(i_lastreview)
        duration = "x"
        i_srspos = str(i_srspos)
        if i_srspos == "[(0,)]":
            items_to_learn += i
        elif i_srspos == "[(1,)]":
            print(datetime.now())
            #need to add if i_lastreview - datetime.now() > 4 hours, add to review stack.
        else:
            print()
    print(items_to_learn)




    available_lessons = len(items_to_learn)


def set_management():  # menu to make changes to selected set
    clear_window()
    description_text = "Select the item you'd like to make changes to:"
    set_management_header = Label(gui, text=global_chosen_set,
                                  font=("Corbel", 30))  # creates a header label, the title of the chosen set
    set_management_header.grid(column=0, row=0, padx="475", pady="10")  # places the header label on the canvas
    set_management_description = Label(gui, text=description_text, font=("Corbel", 15))
    set_management_description.grid(column=0, row=1, padx="20", pady="10")
    items_lb = Listbox(gui, width="50", height="30", selectmode=BROWSE)  #creates a listbox widget to display all items and their prompts and responses
    items_lb.grid(column=0, row=2, padx="320", pady="5")  #places prompt listbox
    mycursor.execute('SELECT ItemID from items WHERE SetID = (%s)' % (global_chosen_setid))  #sql statement to select all itemids from chosen set
    itemids = mycursor.fetchall()  #assigns output of sql statement to itemids variable
    prompts = []
    responses = []
    for itemid in itemids:  #a loop for each itemid, appends the corresponding promptout to a list to be used in the listbox
        mycursor.execute('SELECT PromptOut FROM prompts WHERE ItemID = (%s)' % (itemid))
        prompts.append(mycursor.fetchall())

    for itemid in itemids:  #a loop for each itemid, appends the corresponding responseout to a list to be used in the listbox
        mycursor.execute('SELECT ResponseOut FROM responses WHERE ItemID = (%s)' % (itemid))  #sql statement to
        responses.append(mycursor.fetchall())

    items_list = []  #creates an empty list for prompts and reponses to be inserted to as pairs
    for i in range(len(prompts)):
        prompt_str = str(prompts[i])
        response_str = str(responses[i])
        disallowed_characters = """(),[]\'"""
        for character in disallowed_characters:  # removes all unwanted punctuation from prompt string
            prompt_str = prompt_str.replace(character, "")
        for character in disallowed_characters:  # removes all unwanted punctuation from response string
            response_str = response_str.replace(character, "")
        items_list.append([prompt_str, response_str])
        i+=1

    n=0  #variable to determine position within listbox to insert prompt to, increments with each iteration
    for item in items_list:
        disallowed_characters = "{}[]"
        item=str(item)
        for character in disallowed_characters:  # removes all unwanted punctuation from prompt string
            item = item.replace(character, "")
        items_lb.insert(n, item)  #inserts item to the listbox widget
        n+=1
    def confirm_selection(items_lb):
        selection = items_lb.curselection()
        if selection:
            index = selection[0]
            val = items_lb.get( index  )
            item_manage(val)
    confirm_button = Button(gui, text="Confirm Selection", command= lambda: confirm_selection(items_lb))
    confirm_button.grid(column=0, row=4, pady="10")

def item_manage(val):  #function for management of a specific item
    clear_window()
    print(val)

# OPENING MENU:
logo = PhotoImage(file="logo.png")  # logo
logo_label = Label(image=logo)
logo_label.grid(column=0, row=0, padx="352", pady="50")

browse_text = StringVar()  # "browse sets" button
browse_text.set("Browse Sets")
browse_button = Button(gui, textvariable=browse_text, command=fetch_sets, font="Corbel", height=3,
                       width=30)
browse_button.grid(column=0, row=1, padx="320")

gui.mainloop()  # runs the gui window
