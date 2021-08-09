from tkinter import *

gui = Tk()#creates gui window
gui.title("SimpleSRS")#gives the window a title
gui.geometry("1280x720")

#create menu selection buttons
#logo:
logo = PhotoImage(file="logo.png")
logo_label = Label(image=logo)
logo_label.grid(column=0, row=0, padx="352", pady="50")

#"browse sets" button:
browse_text = StringVar()
browse_button = Button(gui, textvariable=browse_text, font="Corbel", bg="#ffffff", height=3, width=30)
browse_text.set("Browse Sets")
browse_button.grid(column=0, row=1, padx="320")

gui.mainloop()#runs the gui window
