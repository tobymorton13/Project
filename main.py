from tkinter import *
main = Tk()#creates a main root window

def button_clicked():
    text = Label(main,text="you clicked the button")#creates the label variable
    text.pack()
button_1 = Button(main,text="click me",fg="yellow",highlightbackground="blue",command=button_clicked)
button_1.pack()#uses pack method to add button to gui


main.mainloop()#prevent gui window from closing instantly