from tkinter import *
import mysql.connector
from datetime import datetime, timedelta

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
    all_widgets = gui.grid_slaves()  # creates list of all buttons within the gui window
    for widgets in all_widgets:  # clears gui window
        widgets.destroy()


def fetch_sets():  # set selection menu
    clear_window()  # remove opening menu labels/buttons:
    mydb.commit()
    set_select_header = Label(gui, text="Select a set below:", font=("Corbel", 30))  # creates header text label
    set_select_header.grid(column=0, row=0, padx="150")
    row_n = 1  # variable which will increment each set button's vertical position in window
    for item in sets:  # loop to display all sets output from extract statement above as buttons
        item = str(item)[2:-3]  # converts item from tuple to string and removes leading and trailing punctuation
        item.replace(" ", "")
        button = Button(gui, text=item, command=lambda chosen_set=item: set_options(chosen_set), font=("Corbel", 17),
                        height=1, width=15)
        # creates a button displaying the set's name, linking to the set_options function with the chosen set as the function's argument
        button.grid(column=0, row=row_n, padx="520", pady="5")
        row_n += 1
    new_set_btn = Button(gui, text="Create new set", command=new_set, font=("Corbel", 17), width=15,
                         background="skyblue")
    new_set_btn.grid(row=row_n, pady=5)
    row_n += 1  # increment row n variable to ensure quit button is placed below new set button and not on it
    quit_btn = Button(gui, text="Quit", command=gui.destroy, background="firebrick3", foreground="white",
                      font=("Corbel", 17), width=12)
    quit_btn.grid(row=row_n, pady=5)


def new_set():  # function to create widgets for new set creation page
    clear_window()
    new_set_header = Label(gui, text="Enter new set's title below:", font=("Corbel", 30))
    new_set_header.grid(column=0, row=0, pady=20, padx=400)
    new_set_entry = Entry(gui, width=15, font=("Corbel", 15))
    new_set_entry.grid(column=0, row=1, pady=5)
    new_set_confirm = Button(gui, text="Confirm title", command=lambda: new_set_create(new_set_entry), width=15,
                             background="springgreen2")
    new_set_confirm.grid(column=0, row=2, pady=5)
    return_btn = Button(gui, text="Go back", command=lambda: fetch_sets(), height=1, width=15,
                        # creates a 'go back' button
                        background="gray3", foreground="white", font=("Corbel", 13))
    return_btn.grid(column=0, row=3, pady=5)


def new_set_create(new_set_entry):
    set_title = new_set_entry.get()
    if len(set_title) > 25:
        new_set()
        print("invalid set title")
    else:
        set_title=set_title
    mycursor.execute('SELECT SetID FROM sets')  # sql statement to extract all setid's
    setid_list = mycursor.fetchall()  # stores output of statement in a list
    max_setid = max(setid_list)  # calculates the highest setid currently in the database
    max_setid = str(max_setid)
    max_setid = int(remove_punc(max_setid))
    max_setid += 1
    mycursor.execute('INSERT INTO sets (SetID, SetName) values (%s, %s)', (
        max_setid, set_title))  # sql statement to create entry in the database of new set's name and setid
    mydb.commit()
    fetch_sets()


def remove_punc(string):  # function to remove all unwanted punctuation from a string
    disallowed_characters = "{}',()[]"
    for character in disallowed_characters:
        string = string.replace(character, "")
    return string


def review_check(last_rev, max_dur):  # function to verify whether an item is due for a review
    now = datetime.now()
    last_rev = str(last_rev)
    last_rev = remove_punc(last_rev)
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
    set_options_header.grid(column=0, row=0, padx="500")  # places the header label on the canvas
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
    for i in itemid_list:  # loop to verify which items are due for a lesson or review
        i = remove_punc(str(i))  # convert each itemid from tuple to string and remove unwanted punctuation
        mycursor.execute('SELECT repetitions FROM items WHERE ItemID = (%s)' % (
            i))  # sql statement to extract item i's position in the srs system
        i_reps = mycursor.fetchall()  # assigns the number of repetitions of item i to a variable
        i_reps = str(i_reps[0])
        i_reps = remove_punc(i_reps)
        i_reps = int(i_reps)
        mycursor.execute('SELECT LastReview FROM items WHERE ItemID = (%s)' % (
            i))  # sql statement to extract datetime of item i's last review
        i_lastreview = mycursor.fetchall()  # assigns the datetime of item i's last review to a variable
        mycursor.execute('SELECT efactor FROM items WHERE ItemID = (%s)' % (
            i))  # sql statement to extract efactor of item i
        ef = mycursor.fetchall()
        ef = remove_punc(str(ef[0]))
        ef = float(ef)
        interval = (((
                             i_reps - 1) * ef) * 24 * 3600) - 1  # uses sm-2 algorithm to calculate interval for item i in seconds- for n>2: I(n):=I(n-1)*EF
        if i_reps == 0:  # if loop that verifies whether an item is due for a review, calls review_check taking item's last review and calculated interval from sm-2 algorithm, as arguments
            items_to_learn.append(i)
        elif i_reps == 1:
            if review_check(i_lastreview,
                            86399):  # the supermemo sm-2 algorithm states that for the first two repetitions of an item, intervals of 1 day then 6 days should be used, 86399 is one second less than 24 hours
                items_to_review.append(i)
        elif i_reps == 2:
            if review_check(i_lastreview,
                            518399):  # the supermemo sm-2 algorithm states that for the first two repetitions of an item, intervals of 1 day then 6 days should be used, 518399 is one second less than 6*24 hours
                items_to_review.append(i)
        else:
            if review_check(i_lastreview, interval):
                items_to_review.append(i)
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
                         # creates button displaying number of lessons available for the chosen set
                         background="yellow")
    lessons_btn.grid(column=0, row=1, pady="5")
    reviews_btn = Button(gui, text=reviews_btn_text, command=reviews, font=("Corbel", 17), height=2, width=23,
                         # creates button displaying number of reviews available for the chosen set
                         background="yellow")
    reviews_btn.grid(column=0, row=2, pady="5")
    set_manage_button = Button(gui, text="Edit Set", command=set_management, background="steelblue",
                               font=("Corbel", 13), height=1, width=15)  # edit a "manage set" button
    set_manage_button.grid(column=0, row=3, pady="2")  # places the manage set button on the canvas
    set_delete_btn = Button(gui, text="Delete Set", command=delete_set, background="firebrick3", height=1,
                            width=15, font=("Corbel", 13))  # creates button allowing user to delete set
    set_delete_btn.grid(column=0, row=4, pady=2)
    return_btn = Button(gui, text="Go back", command=lambda: fetch_sets(), height=1, width=15,
                        background="gray3", foreground="white", font=("Corbel", 13))  # creates a 'go back' button
    return_btn.grid(column=0, row=5, pady="2")


def delete_set():  # function used to delete chosen set, called by 'delete set' button
    mycursor.execute('SELECT ItemID FROM items WHERE SetID = (%s)' % (global_chosen_setid))
    itemids = mycursor.fetchall()
    for id in itemids:
        mycursor.execute('DELETE FROM prompts WHERE ItemID = (%s)' % (id))  # deletes all prompts for selected itemid
        mycursor.execute('DELETE FROM responses WHERE ItemID = (%s)' % (id))  # deletes all responses for selected itemid
        mycursor.execute(
            'DELETE FROM items WHERE ItemID = (%s)' % (id))  # deletes all in the items table for selected itemid
    mycursor.execute('DELETE FROM sets WHERE SetID = (%s)' % (global_chosen_setid))   # deletes the set id and setname from the sets table
    mydb.commit()
    fetch_sets()



def lessons():  # function used when user begins lessons
    clear_window()
    for item in global_items_to_learn:  # iterates over the items to learn list, carries out the lesson loop for each item
        clear_window()
        item = int(item)
        mycursor.execute('SELECT PromptOut FROM prompts WHERE ItemID = (%s)' % (item))
        prompt = mycursor.fetchall()
        prompt_lbl_text = str(prompt[0])  # variable containing the prompt to be used in the header label
        prompt_lbl_text = remove_punc(prompt_lbl_text)
        prompt_lbl = Label(gui, text=prompt_lbl_text,
                           font=("Corbel", 40))  # creates label displaying current items prompt
        prompt_lbl.grid(column=0, row=0, pady="10")
        global show_response_btn
        show_response_btn = Button(gui, text="Show Response",
                                   command=lambda: lesson_show_response(item, prompt_lbl_text),
                                   font=("Corbel", 25), background="springgreen2", )
        show_response_btn.grid(column=0, row=2, pady=20, padx=500)
        return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=15,
                            background="gray3", foreground="white", font=("Corbel", 13))
        return_btn.grid(column=0, row=3, pady="2")
    if not global_items_to_learn:  # if items to learn list is empty, return to the set options menu
        set_options(global_chosen_set)


def lesson_show_response(item, prompt_lbl_text):
    show_response_btn.destroy()
    mycursor.execute('SELECT ResponseOut FROM responses WHERE ItemID = (%s)' % (
        item))  # extracts correct response from database for selected itemid
    correct_response = mycursor.fetchall()
    correct_response = str(correct_response[0])  # sets correct_response variable as a string
    correct_response = remove_punc(correct_response)  # removes unwanted punctuation from correct response string
    correct_response_lbl = Label(gui, text=correct_response, font=("Corbel", 35))
    correct_response_lbl.grid(column=0, row=2)
    hide_response_btn = Button(gui, text="Hide Response",
                               command=lambda: lesson_hide_response(item, correct_response, prompt_lbl_text),
                               font=("Corbel", 25), background="black",
                               foreground="white")  # creates a button to allow  the user to hide the response when they are ready to enter it themself
    hide_response_btn.grid(column=0, row=3, pady=20, padx=500)
    return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=15,
                        background="gray3", foreground="white",
                        font=("Corbel", 13))  # creates a 'go back' button to return to set_options menu
    return_btn.grid(column=0, row=4, pady="2")


def lesson_hide_response(item, correct_response, prompt_lbl_text):
    clear_window()
    prompt_header = Label(gui, text=prompt_lbl_text, font=("Corbel", 35))
    prompt_header.grid(column=0, row=0)
    response_entry_instruct = Label(gui, text="Enter the response below:", font=("Corbel", 30))
    response_entry_instruct.grid(column=0, row=1)
    lesson_user_entry = Entry(gui, width=30,
                              font=("Corbel", 15))  # creates entry box for user to enter response to prompt
    lesson_user_entry.grid(column=0, row=2)
    entry_confirm_btn = Button(gui, text="Confirm Response",
                               command=lambda: lesson_confirm_response(item, lesson_user_entry, correct_response),
                               font=("Corbel", 25), background="springgreen2", )
    entry_confirm_btn.grid(column=0, row=3, pady=20, padx=500)
    return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=15,
                        background="gray3", foreground="white", font=("Corbel", 13))
    return_btn.grid(column=0, row=4, pady="2")


def lesson_confirm_response(item, lesson_user_entry,
                            correct_response):  # function to verify whether the user's response matches the correct response stored in the database
    user_input = lesson_user_entry.get()  # assigns the user's inputted response to the user_input variable
    user_input = remove_punc(user_input)
    user_input.lower()  # ensures user response is all lower case to prevent correct response being flagged as incorrect
    lowercase_correct_response = correct_response.lower()  # ensures correct response is all lower case to prevent correct response being flagged as incorrect
    if user_input == lowercase_correct_response:  # if user enters correct response:
        clear_window()
        reps_update_statement = 'UPDATE items SET repetitions = (%s) WHERE ItemID = (%s)'  # sql statement to increase the item's repetitions by 1 if the correct response is entered by the user
        reps_update_data = (1, item)  # variable storing data to be used in sql update statement
        mycursor.execute(reps_update_statement, reps_update_data)
        mydb.commit()
        now = str(datetime.now())
        lastreview_update_statement = 'UPDATE items SET LastReview = (%s) WHERE ItemID = (%s)'  # sql statement to update the lastreview datetime of the item to the current datetime if the correct response is entered by the user.
        lastreview_update_data = (now,
                                  item)  # stores the current datetime and the item id in a single object, to allow query to be executed with only 2 arguments
        mycursor.execute(lastreview_update_statement, lastreview_update_data)
        mydb.commit()
        lesson_next_item(item)  # calls the next item function
        n_update_statement = 'UPDATE items SET repetitions = (%s) WHERE ItemID = (%s)'  # sql statement to reset item's repetitions to 1, following sm-2 algorithm's rules for when response grade is below 3
        n_update_data = (1, item)
        mycursor.execute(n_update_statement, n_update_data)
        mydb.commit()
    else:  # if user enters incorrect response:
        clear_window()
        incorrect_lbl = Label(gui, text="Incorrect, the correct response was:",
                              font=("Corbel", 35))  # label stating user's response was incorrect
        incorrect_lbl.grid(column=0, row=0, padx="270", pady="10")
        correct_response_lbl = Label(gui, text=correct_response, font=("Corbel", 30),
                                     foreground="grey")  # label showing correct response
        correct_response_lbl.grid(column=0, row=1, pady="10")
        user_entry_2 = Entry(gui, width=30,
                             font=("Corbel", 15))  # creates entry box for user to enter correct response to prompt
        user_entry_2.grid(column=0, row=2)
        entry_confirm_btn = Button(gui, text="Confirm Response",
                                   command=lambda: lesson_confirm_response(item, user_entry_2, correct_response),
                                   font=("Corbel", 25), background="springgreen2", )
        entry_confirm_btn.grid(column=0, row=3, pady=20)
        return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=15,
                            background="gray3", foreground="white", font=("Corbel", 13))
        return_btn.grid(column=0, row=4, pady="2")


def lesson_next_item(
        item):  # function to remove the completed item from the review list and call the function to progress onto the next item.
    clear_window()

    item = str(item)  # converts item from int back to string to allow it to be found and removed from review list
    global_items_to_learn.remove(item)  # removes the completed item from
    lessons()


def reviews():  # function used when user begins reviews
    clear_window()
    for item in global_items_to_review:
        clear_window()
        item = int(item)
        mycursor.execute('SELECT PromptOut FROM prompts WHERE ItemID = (%s)' % (
            item))  # sql statement to extract prompt from database for selected item id
        prompt = mycursor.fetchall()
        prompt_lbl_text = str(prompt[0])
        prompt_lbl_text = remove_punc(prompt_lbl_text)
        prompt_lbl = Label(gui, text=prompt_lbl_text, font=("Corbel", 40))
        prompt_lbl.grid(column=0, row=0, pady="10")
        user_entry = Entry(gui, width=30, font=("Corbel", 15))  # creates entry box for user to enter response to prompt
        user_entry.grid(column=0, row=1)
        entry_confirm_btn = Button(gui, text="Confirm Response",
                                   command=lambda: review_confirm_response(item, user_entry),
                                   font=("Corbel", 25),
                                   background="springgreen2", )  # creates a button for the user to confirm their response
        entry_confirm_btn.grid(column=0, row=2, pady=20, padx=470)
        return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=15,
                            # creates a 'go back' button to return to the set options menu
                            background="gray3", foreground="white", font=("Corbel", 13))
        return_btn.grid(column=0, row=3, pady="2")
    if not global_items_to_review:  # if the items to review list is empty, return to the set options menu
        set_options(global_chosen_set)


def review_confirm_response(item, user_entry):  # function to
    user_input = user_entry.get()
    mycursor.execute('SELECT ResponseOut FROM responses WHERE ItemID = (%s)' % (
        item))  # extracts correct response from database for selected itemid
    correct_response = mycursor.fetchall()
    correct_response = str(correct_response[0])  # sets correct_response variable as a string
    correct_response = remove_punc(correct_response)
    user_input = remove_punc(user_input)
    user_input = user_input.lower()  # ensures user response is all lower case to prevent correct response being flagged as incorrect
    lowercase_correct_response = correct_response.lower()  # ensures correct response is all lower case to prevent correct response being flagged as incorrect
    if user_input == lowercase_correct_response:  # if user enters correct response:
        clear_window()
        now = str(datetime.now())
        lastreview_update_statement = 'UPDATE items SET LastReview = (%s) WHERE ItemID = (%s)'  # sql statement to update the lastreview datetime of the item to the current datetime if the correct response is entered by the user.
        lastreview_update_data = (now,
                                  item)  # stores the current datetime and the item id in a single object, to allow query to be executed with only 2 arguments
        mycursor.execute(lastreview_update_statement, lastreview_update_data)
        mydb.commit()
        correct_lbl = Label(gui, text="Correct",
                            font=("Corbel", 40), padx=250,
                            fg="green")  # creates label stating user's response was incorrect
        correct_lbl.grid(column=0, row=0, padx="270", pady="10")
        rate_response_lbl = Label(gui, text="Grade your response:",
                                  font=("Corbel", 30))  # creates label prompting user to grade their response
        rate_response_lbl.grid(column=0, row=2, pady=5)
        rate_3 = Button(gui, text="C: Very difficult to recall correct response",
                        command=lambda: review_next_item(item, 3), font=("Corbel", 15),
                        background="red", width=35)  # creates button for user to rate response
        rate_3.grid(column=0, row=5, pady=5)
        rate_4 = Button(gui, text=" B: Correct response after hesitation", command=lambda: review_next_item(item, 4),
                        font=("Corbel", 15), background="yellow", width=35)  # creates button for user to rate response
        rate_4.grid(column=0, row=4, pady=5)
        rate_5 = Button(gui, text="A: Correct response straight away",
                        command=lambda: review_next_item(item, 5), font=("Corbel", 15),
                        background="springgreen2", width=35)  # creates button for user to rate response
        rate_5.grid(column=0, row=3, pady=5)
    else:  # if user enters incorrect response:
        clear_window()
        incorrect_lbl = Label(gui, text="Incorrect, the correct response was:",
                              font=("Corbel", 35))  # creates label stating user's response was incorrect
        incorrect_lbl.grid(column=0, row=0, padx="270", pady="10")
        correct_response_lbl = Label(gui, text=correct_response, font=("Corbel", 30), foreground="grey")
        correct_response_lbl.grid(column=0, row=1, pady="10")  # creates label displaying the correct response
        rate_response_lbl = Label(gui, text="Grade your response:", font=("Corbel", 25))
        rate_response_lbl.grid(column=0, row=2, pady=5)  # creates label prompting user to grade their response
        rate_0 = Button(gui, text="C: Complete blackout", command=lambda: review_next_item(item, 0),
                        font=("Corbel", 15), background="red", width=50)
        rate_0.grid(column=0, row=5,
                    pady=5)  # creates button for user to rate response, calls review_next_item function when pressed
        rate_1 = Button(gui, text="B: Remembered correct response when shown",
                        command=lambda: review_next_item(item, 1), font=("Corbel", 15), background="yellow", width=50)
        rate_1.grid(column=0, row=4,
                    pady=5)  # creates button for user to rate response, calls review_next_item function when pressed
        rate_2 = Button(gui, text="A: Correct response seemed easy to recall before answering",
                        command=lambda: review_next_item(item, 2), font=("Corbel", 15), background="springgreen2",
                        width=50)
        rate_2.grid(column=0, row=3,
                    pady=5)  # creates button for user to rate response, calls review_next_item function when pressed
        return_btn = Button(gui, text="Go back", command=lambda: set_options(global_chosen_set), height=1, width=15,
                            background="gray3", foreground="white", font=("Corbel", 13))  # creates a 'go back' button
        return_btn.grid(column=0, row=6, pady=2)


def review_next_item(
        item,
        q):  # function to remove the completed item from the review list and call the function to progress onto the next item.
    clear_window()
    mycursor.execute('SELECT repetitions FROM items WHERE ItemID = %s' % (
        item))  # sql statement to extract repetitions from items table
    n = mycursor.fetchall()  # assigns n to the output of the sql statement, n is the number of repetitions of the item
    mycursor.execute(
        'SELECT efactor FROM items WHERE ItemID = %s' % (item))  # sql statement to extract repetitions from items table
    ef = mycursor.fetchall()  # assigns ef to the output of the sql statement, ef is the efactor of an item- its estimated difficulty.
    ef = remove_punc(str(ef))
    ef = float(ef)
    if q < 3:  # if user answers incorrectly, causing response rating to be less than 3, the item is reset to the beginning of the SR system, following sm-2 algorithm's rules.
        ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))  # calculate item's new efactor, following SM-2 procedure
        if ef < 1.3:  # if calculated efactor is less than 1.3, assign it to 1.3, following SM-2 procedure
            ef = 1.3
        else:
            ef = ef
        now = str(datetime.now())
        lastreview_update_statement = 'UPDATE items SET LastReview = (%s) WHERE ItemID = (%s)'  # sql statement to update the lastreview datetime of the item to the current datetime if the correct response is entered by the user.
        lastreview_update_data = (now, item)  # stores the current datetime and the item id in a single object, to allow query to be executed with only 2 arguments
        mycursor.execute(lastreview_update_statement, lastreview_update_data)
        mydb.commit()
        ef_update_statement = 'UPDATE items SET efactor = (%s) WHERE ItemID = (%s)'  # sql statement to reset item's efactor to 2.5, following sm-2 algorithm's rules for when response grade is below 3
        ef_update_data = (ef, item)
        mycursor.execute(ef_update_statement, ef_update_data)
        mydb.commit()
        n_update_statement = 'UPDATE items SET repetitions = (%s) WHERE ItemID = (%s)'  # sql statement to reset item's repetitions to 1, following sm-2 algorithm's rules for when response grade is below 3
        n_update_data = (1, item)
        mycursor.execute(n_update_statement, n_update_data)
        mydb.commit()
        global_items_to_review.pop()
    elif q >= 3 and q <= 5:  # if user responds correctly, follow sm-2 procedure to calculate new efactor and update item's reps an
        ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))  # calculate item's new efactor, following SM-2 procedure
        if ef < 1.3:  # if calculated efactor is less than 1.3, assign it to 1.3, following SM-2 procedure
            ef = 1.3
        else:
            ef = ef
        ef_update_statement = 'UPDATE items SET efactor = (%s) WHERE ItemID = (%s)'  # sql statement to update the lastreview datetime of the item to the current datetime if the correct response is entered by the user.
        ef_update_data = (ef,
                          item)  # stores the current datetime and the item id in a single object, to allow query to be executed with only 2 arguments
        mycursor.execute(ef_update_statement,
                         ef_update_data)  # sql statement to update item's efactor to new calculated value
        mydb.commit()
        n = remove_punc(str(n[0]))  # removes all punctuation from n so it can be converted to an integer
        n = int(n)  # convert n to an integer to allow it to be inserted into items table
        n += 1  # increment n by 1 to reflect that the user has completed a review
        n_update_statement = 'UPDATE items SET repetitions = (%s) WHERE ItemID = (%s)'  # sql statement to update item's repetitions count
        n_update_data = (n, item)
        mycursor.execute(n_update_statement, n_update_data)  # executes sql statement taking 'n' repetitions and item as the data for the query
        mydb.commit()
        item = str(item)
        global_items_to_review.pop()  # since the user answered correctly, pop the item from the review stack
    else:
        reviews()
    q = 0  # reassign q to 0 to prevent the last known value being used if user closes the program before grading their response
    reviews()


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
    chosen_itemid = remove_punc(str(chosen_itemid))
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
    if len(new_prompt) > 60:
        set_options(global_chosen_set)
    new_response = new_response_entry.get()  # assigns the new response input by the user to a variable
    if len(new_response) > 60:
        set_options(global_chosen_set)
    max = max_item_id()  # call this function so the new item's itemid can be an increment of the previous max value
    max = str(max)
    disallowed_characters = "(),[]"
    for character in disallowed_characters:  # removes all unwanted punctuation from chosen item id
        max = max.replace(character, "")
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
    if len(new_prompt) > 60:
        set_options(global_chosen_set)
    prompt_statement = 'UPDATE prompts SET PromptOut = (%s) WHERE ItemID = (%s)'
    data = (new_prompt, chosen_itemid)
    mycursor.execute(prompt_statement, data)
    mydb.commit()


def response_confirm():  # function to update the response table with the new updates entered by the user
    new_response = response_entry.get()  # assigns the new response input by the user to a variable
    if len(new_response) > 60:
        set_options(global_chosen_set)
    response_statement = 'UPDATE responses SET ResponseOut = (%s) WHERE ItemID = (%s)'
    data = (new_response, chosen_itemid)
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
