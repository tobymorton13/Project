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
gui.geometry("1280x750")  # resizes window to 1280x720p


def clear_window():  # function used whenever a new page is loaded and all widgets from previous menu need to be cleared
    all_buttons = gui.grid_slaves()  # creates list of all buttons within the gui window
    for buttons in all_buttons:  # clears gui window
        buttons.destroy()


def fetch_sets():  # set selection menu
    clear_window()  # remove opening menu labels/buttons:
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
    quit_btn = Button(gui, text="Quit", command=gui.destroy, background="firebrick3", foreground="white",
                      font=("Corbel", 17), width=12)
    quit_btn.grid(row=row_n, pady=5)


def remove_punc(string):  # function to remove all unwanted punctuation from a string
    disallowed_characters = "{}',()[]"
    for character in disallowed_characters:
        string = string.replace(character, "")
    return string


def review_check(last_rev, max_dur):  # function to verify whether an item is due for a review
    now = datetime.now()
    last_rev = str(last_rev)
    disallowed_characters = "(),[]'"  # creation of a set of unwanted punctuation
    for character in disallowed_characters:  # removes all unwanted puctuation from 'i' to allow it to be used it the sql select statement
        last_rev = last_rev.replace(character, "")
    x = last_rev
    if (x[5] == "0") and (x[8] == "0"):
        last_rev_datetime = datetime(int(x[0:4]), int(x[6]), int(x[9]), int(x[11:13]), int(x[14:16]), int(x[17:19]))
    elif (x[5] == "0"):
        last_rev_datetime = datetime(int(x[0:4]), int(x[6]), int(x[8:10]), int(x[11:13]), int(x[14:16]), int(x[17:19]))
    elif (x[8] == "0"):
        last_rev_datetime = datetime(int(x[0:4]), int(x[5:7]), int(x[9]), int(x[11:13]), int(x[14:16]), int(x[17:19]))
    else:
        last_rev_datetime = datetime(int(x[0:4]), int(x[5:7]), int(x[8:10]), int(x[11:13]), int(x[14:16]),
                                     int(x[17:19]))
    duration = now - last_rev_datetime
    if duration.total_seconds() > max_dur:
        return (True)
    else:
        return (False)


def set_options(chosen_set):  # chosen set option menu, from here, lessons, reviews and edits to set can be completed
    clear_window()
    global global_chosen_set  # creation of a global chosen_set variable to allow it to be used in the set management screen
    global_chosen_set = chosen_set
    set_options_header = Label(gui, text=chosen_set,
                               font=("Corbel", 30))  # creates a header label, the title of the chosen set
    set_options_header.grid(column=0, row=0, padx="475")  # places the header label on the canvas
    mycursor.execute('SELECT SetID, SetName FROM sets')  # sql statement to select all setid's and setnames
    set_list = mycursor.fetchall()  # assign output of sql statement to set_list variable
    tuple_in_list = [set_list for set_list in set_list if
                     chosen_set in set_list]  # outputs tuple within list that contains chosen_set
    chosen_setid = (str(tuple_in_list))[2]  # selects character of output tuple that correponds to chosen set's setid
    global global_chosen_setid  # creation of a global chosen_setid variable to allow it to be used in the set management screen
    global_chosen_setid = chosen_setid
    mycursor.execute(
        'SELECT items.ItemID FROM Items INNER JOIN sets ON Items.SetID = sets.SetID WHERE sets.SetID = (%s)' % (
            chosen_setid))
    itemid_list = mycursor.fetchall()
    items_to_learn = []  # creates empty list to store items due for lesson
    items_to_review = []  # creates empty list to store items due for review
    learned_item_count = 0  # will be used to calculate set completion
    total_item_count = 0  # ^^^
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
        i_srspos = str(i_srspos)
        if i_srspos == "[(0,)]":  # if loop verifies whether an item is due for a review, calls review check taking item's last review and max duration, dependent on srs pos as arguments
            items_to_learn.append(i)
        elif i_srspos == "[(1,)]":
            if review_check(i_lastreview, 14399):
                items_to_review.append(i)
        elif i_srspos == "[(2,)]":
            if review_check(i_lastreview, 28799):
                items_to_review.append(i)
        elif i_srspos == "[(3,)]":
            if review_check(i_lastreview, 86399):
                items_to_review.append(i)
        elif i_srspos == "[(4,)]":
            if review_check(i_lastreview, 172799):
                items_to_review.append(i)
        elif i_srspos == "[(5,)]":
            if review_check(i_lastreview, 647999):
                items_to_review.append(i)
        elif i_srspos == "[(6,)]":
            if review_check(i_lastreview, 1295999):
                items_to_review.append(i)
        elif i_srspos == "[(7,)]":
            if review_check(i_lastreview, 2591999):
                items_to_review.append(i)
        elif i_srspos == "[(8,)]":
            if review_check(i_lastreview, 10367999):
                items_to_review.append(i)
        else:
            learned_item_count += 1
        total_item_count += 1
    available_lesson_count = str(len(items_to_learn))
    available_review_count = str(len(items_to_review))
    global global_items_to_learn  # adds global versions of lesson/review lists to allow them to be used in other functions
    global_items_to_learn = items_to_learn
    global global_items_to_review
    global_items_to_review = items_to_review
    if available_lesson_count == "1":  # adjusts string based on whether plural for lesson is appropriate
        lessons_btn_text = ("You have " + available_lesson_count + " lesson available")
    else:
        lessons_btn_text = ("You have " + available_lesson_count + " lessons available")
    if available_review_count == "1":
        reviews_btn_text = ("You have " + available_review_count + " review available")
    else:
        reviews_btn_text = ("You have " + available_review_count + " reviews available")
    lessons_btn = Button(gui, text=lessons_btn_text, command=lessons, font=("Corbel", 17), height=2, width=23,
                         background="yellow")
    lessons_btn.grid(column=0, row=1, pady="5")
    reviews_btn = Button(gui, text=reviews_btn_text, command=reviews, font=("Corbel", 17), height=2, width=23,
                         background="yellow")
    reviews_btn.grid(column=0, row=2, pady="5")
    set_manage_button = Button(gui, text="Edit Set", command=set_management, background="gray3", foreground="white",
                               font=("Corbel", 13), height=1,
                               width=15)  # edit a "manage set" button
    set_manage_button.grid(column=0, row=3, pady="2")  # places the manage set button on the canvas
    return_btn = Button(gui, text="Go back", command=lambda: fetch_sets(), height=1, width=15,
                        background="gray3", foreground="white", font=("Corbel", 13))
    return_btn.grid(column=0, row=4, pady="2")


def lessons():  # function used when user begins lessons
    clear_window()


def reviews():  # function used when user begins reviews
    clear_window()
    i=0
    review_count = len(global_items_to_review)
    for i in range(review_count):
        clear_window()
        item = int(global_items_to_review[0])
        mycursor.execute(
            'SELECT PromptOut FROM prompts WHERE ItemID = (%s)' % (item))  # extracts the prompt for the current itemID
        prompt = remove_punc(
            str(mycursor.fetchall()))  # assigns output of sql statement with all unwanted punctuation removed, to prompt variable
        print(prompt)
        review_header = Label(gui, text=prompt, font=("Corbel", 28))  # creates a header, the current item's prompt
        review_header.grid(column=0, row=0, padx=450, pady=30)
        review_instruction = Label(gui, text="Enter your response below:", font=("Corbel", 18))
        review_instruction.grid(column=0, row=1)
        review_entry = Entry(gui, width=27, font=("Corbel", 13))
        review_entry.grid(column=0, row=2, pady=10)
        review_confirm_btn = Button(gui, text="Confirm", width=17,
                                    background="springgreen2", command = lambda: verify_response(review_entry, item), font=("Corbel", 15), height=1)
        review_confirm_btn.grid(column=0, row=3)
        global review_outcome
        review_outcome = False
        while review_outcome is False:



def verify_response(user_input, item):
    mycursor.execute('SELECT ResponseOut FROM responses WHERE ItemID = (%s)' % (item))
    correct_response = remove_punc(str(mycursor.fetchall()[0]))
    user_response = user_input.get()
    print(correct_response)
    print(user_response)
    if user_response.lower() == correct_response.lower():
        print("correct")
        review_outcome = True
    else:
        print("incorrect")
        review_outcome = False





def set_management():  # menu to make changes to selected set
    clear_window()
    description_text = "Select the item you'd like to make changes to:"
    set_management_header = Label(gui, text=global_chosen_set,
                                  font=("Corbel", 30))  # creates a header label, the title of the chosen set
    set_management_header.grid(column=0, row=0, padx="475", pady="10")  # places the header label on the canvas
    set_management_description = Label(gui, text=description_text, font=("Corbel", 15))
    set_management_description.grid(column=0, row=1, padx="20", pady="10")
    items_lb = Listbox(gui, width="50", height="30",
                       selectmode=BROWSE)  # creates a listbox widget to display all items and their prompts and responses
    items_lb.grid(column=0, row=2, padx="320", pady="5")  # places prompt listbox
    mycursor.execute('SELECT ItemID from items WHERE SetID = (%s)' % (
        global_chosen_setid))  # sql statement to select all itemids from chosen set
    itemids = mycursor.fetchall()  # assigns output of sql statement to itemids variable
    prompts = []
    responses = []
    for itemid in itemids:  # a loop for each itemid, appends the corresponding promptout to a list to be used in the listbox
        mycursor.execute('SELECT PromptOut FROM prompts WHERE ItemID = (%s)' % (itemid))
        prompts.append(mycursor.fetchall())

    for itemid in itemids:  # a loop for each itemid, appends the corresponding responseout to a list to be used in the listbox
        mycursor.execute('SELECT ResponseOut FROM responses WHERE ItemID = (%s)' % (itemid))  # sql statement to
        responses.append(mycursor.fetchall())

    items_list = []  # creates an empty list for prompts and reponses to be inserted to as pairs
    for i in range(len(prompts)):
        prompt_str = str(prompts[i])
        response_str = str(responses[i])
        disallowed_characters = """(),[]\'"""
        for character in disallowed_characters:  # removes all unwanted punctuation from prompt string
            prompt_str = prompt_str.replace(character, "")
        for character in disallowed_characters:  # removes all unwanted punctuation from response string
            response_str = response_str.replace(character, "")
        items_list.append([prompt_str, response_str])
        i += 1

    n = 0  # variable to determine position within listbox to insert prompt to, increments with each iteration
    for item in items_list:
        disallowed_characters = "{}[]"
        item = str(item)
        for character in disallowed_characters:  # removes all unwanted punctuation from prompt string
            item = item.replace(character, "")
        items_lb.insert(n, item)  # inserts item to the listbox widget
        n += 1

    def confirm_selection(items_lb):
        selection = items_lb.curselection()
        if selection:  # once a selection has been made, if statement is triggered.
            index = selection[0]  # stores the index of the selected item as a variable, also equal to the item's itemid
            val = items_lb.get(index)
            item_manage(val)

    confirm_btn = Button(gui, text="Confirm Selection", command=lambda: confirm_selection(items_lb),
                         background="springgreen2", font=(
            "Corbel", 13))  # button to confirm selection of an item, triggers confirm_selection function
    confirm_btn.grid(column=0, row=4, pady="2")
    new_item_btn = Button(gui, text="New Item...", command=lambda: new_item(), background="sky blue", width=17,
                          font=("Corbel", 13))
    new_item_btn.grid(column=0, row=5, pady="2")
    return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=20,
                        background="gray3", foreground="white", font=("Corbel", 13))
    return_btn.grid(column=0, row=6, pady="2")


def item_manage(val):  # function for management of a specific item
    clear_window()
    item_label = Label(gui, text=val, font=("Corbel", 25))  # creates a header of the selected item
    item_label.grid(column=0, row=0)

    prompt_label = Label(gui, text="Enter the updated prompt:", font=(
        "Corbel", 15))  # creates a label prompting the user to enter a new prompt in the text box
    prompt_label.grid(column=0, row=1, padx=480, pady=1)

    prompt_out = val.split(",")[
        0]  # splits the item string into just the prompt, so it can be used in a select statement to select the relevant itemid
    mycursor.execute('SELECT ItemID FROM prompts WHERE PromptOut = (%s)' % (prompt_out))  # selects chosen item's itemid
    global chosen_itemid
    chosen_itemid = mycursor.fetchall()
    chosen_itemid = str(chosen_itemid)
    disallowed_characters = "(),[]"
    for character in disallowed_characters:  # removes all unwanted punctuation from chosen item id
        chosen_itemid = chosen_itemid.replace(character, "")
    chosen_itemid = int(chosen_itemid)

    global prompt_entry
    prompt_entry = Entry(gui)  # creates a text entry box
    prompt_entry.grid(column=0, row=2, pady=10)
    prompt_entry_btn = Button(gui, text="Confirm changes", command=lambda: prompt_confirm(), height=1, width=13,
                              font=("Corbel", 8))  # creates a confirmation button for the entry of a new prompt
    prompt_entry_btn.grid(column=0, row=3)

    response_label = Label(gui, text="Enter the updated response:", font=(
        "Corbel", 15))  # creates a label prompting the user to enter a new response in the text box
    response_label.grid(column=0, row=4, pady=0)
    global response_entry
    response_entry = Entry(gui)  # creates a text entry box
    response_entry.grid(column=0, row=5, pady=10)
    response_entry_btn = Button(gui, text="Confirm changes", command=lambda: response_confirm(), height=1, width=13,
                                font=("Corbel", 8))  # creates a confirmation button for the entry of a new response
    response_entry_btn.grid(column=0, row=6)

    item_delete_btn = Button(gui, text="Delete Item", command=lambda: item_delete_func(), height=1, width=15,
                             font=("Corbel", 15), background="firebrick3",
                             foreground="white")  # creates an item delete button
    item_delete_btn.grid(column=0, row=7, pady=20)

    return_btn = Button(gui, text="Go back", command=lambda: set_management(), height=1, width=20, background="gray3",
                        foreground="white", font=("Corbel", 13))
    return_btn.grid(column=0, row=8, pady=2)


def new_item():  # function for page allowing creation of a new item
    clear_window()
    new_prompt_header = Label(gui, text="Enter a new prompt:",
                              font=("Corbel", 20))  # creates a label prompting user to input their new item's prompt
    new_prompt_header.grid(column=0, row=0, pady=10, padx=500)
    global new_prompt_entry
    new_prompt_entry = Entry(gui)  # creates a text entry box
    new_prompt_entry.grid(column=0, row=1)
    new_response_header = Label(gui, text="Enter a new response:", font=("Corbel", 20))
    new_response_header.grid(column=0, row=3, pady=10)
    global new_response_entry
    new_response_entry = Entry(gui)
    new_response_entry.grid(column=0, row=4)
    new_item_confirm_btn = Button(gui, text="Confirm prompt and response", command=lambda: create_new_item(), height=1,
                                  width=25, background="springgreen2", font=(
            "Corbel", 18))  # creates a confirmation button which calles the create_new_item function when pressed
    new_item_confirm_btn.grid(column=0, row=5, pady=30)
    return_btn = Button(gui, text="Go back", command=lambda: set_management(), height=1, width=20, background="gray3",
                        foreground="white", font=("Corbel", 13))
    return_btn.grid(column=0, row=6, pady="2")


def create_new_item():  # function to insert new item and its prompt and response to database
    new_prompt = new_prompt_entry.get()  # assigns the new prompt input by the user to a variable
    new_response = new_response_entry.get()  # assigns the new response input by the user to a variable
    max = max_item_id()  # call this function so the new item's itemid can be an increment of the previous max value
    max = remove_punc(str(max))
    max = int(max)  # converts max back to int datatype to allow it to be inserted to table
    max += 1  # increments the previous max itemid by 1 to allow for the variable's use as the new itemid
    now = datetime.now()
    formatted_date = now.strftime(
        '%Y-%m-%d %H:%M:%S')  # reformats the current time to allow it to be inserted to database
    mycursor.execute('INSERT INTO items (ItemID, LastReview, SetID) values(%s, %s, %s)',
                     (max, formatted_date, global_chosen_setid))  # inserts new values to items table
    mydb.commit()
    mycursor.execute('INSERT INTO prompts (ItemID, PromptOut) values(%s, %s)',
                     (max, new_prompt))  # inserts new promptout and relevant itemid to prompts table
    mycursor.execute('INSERT INTO responses (ItemID, ResponseOut) values(%s, %s)',
                     (max, new_response))  # inserts new responseout and relevant itemid to responses table
    mydb.commit()
    set_management()


def max_item_id():  # function to find the highest item id value
    mycursor.execute('SELECT ItemID FROM items')
    itemid_list = mycursor.fetchall()
    x = max(itemid_list)
    return (x)


def prompt_confirm():  # function to update the prompts table with the new updates entered by the user
    new_prompt = prompt_entry.get()  # assigns the user's new prompt input to a variable
    prompt_statement = 'UPDATE prompts SET PromptOut = (%s) WHERE ItemID = (%s)'
    data = (new_prompt, chosen_itemid)
    mycursor.execute(prompt_statement, data)
    mydb.commit()


def response_confirm():  # function to update the response table with the new updates entered by the user
    new_response = response_entry.get()
    response_statement = 'UPDATE responses SET ResponseOut = (%s) WHERE ItemID = (%s)'
    data = (new_response, chosen_itemid)  #
    mycursor.execute(response_statement, data)
    mydb.commit()


def item_delete_func():  # function used to delete an item when the delete button is selected by the user
    mycursor.execute('DELETE FROM prompts WHERE ItemID = (%s)' % (
        chosen_itemid))  # deletes all rows in prompts table corresponding to chosen itemid
    mycursor.execute('DELETE FROM responses WHERE ItemID = (%s)' % (
        chosen_itemid))  # deletes all rows in responses table corresponding to chosen itemid
    mycursor.execute('DELETE FROM items WHERE ItemID = (%s)' % (
        chosen_itemid))  # deletes all rows in items table corresponding to chosen itemid
    mydb.commit()
    set_management()


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
