import time
from tkinter import *
import tkinter as tk
#from tkinter import ttk
#import tkinter.scrolledtext as Text1
from tkinter import Menu
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import font# , colorchooser, filedialog, messagebox
# import os
from datetime import date
from datetime import datetime
from database import fetch_exams

# test
title = ""
qustion = ""
for item in fetch_exams():
    title = item[1]
    qustion = item[2]

created = datetime.now()
ended = datetime.now()

window=Tk()
window.title(title)
w= "700"
h= "600"
window.geometry(w+"x"+h)
window.config(bg='#345')


pane = Frame(window)
pane.pack(fill = 'x', ipady=10)

def stopdef():
    print(window.winfo_reqwidth())



# stop = Button(pane, text = "Stop",
#             background = "red", fg = "white", font=('Digital-7', 20), relief=GROOVE)
stop= Button(pane, text='Stop', font=('Digital-7', 20), bg='red', fg='white', relief=RAISED, command=stopdef) # padx=w1/2, # pady=10, # bd=2
stop.pack(side = LEFT, expand = True, fill = 'both')

date = date.today()
now = datetime.now()
time = now.strftime("%H:%M:%S")

Time = Label(pane, text = f"{time}", background="black", foreground = "red", font=('Digital-7', 20), relief=RIDGE)
Time.pack(side = LEFT, expand = True, fill = 'both')

def Update():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    Time.config(text = f"{time}")
    Time.after(1000, Update)

pane1 = Frame(window, bg="#345",)
pane1.pack(fill = BOTH, expand = True)

questions = tk.Label(pane1, bg="#f5f5f5", bd=4, relief=RAISED, text = qustion, font=('Digital-7', 14), wraplength=w, height=5, background="#345", foreground = "white")
questions.place(relx=0.1, rely=0.5, relheight=0.4, relwidth=0.8)
questions.pack(side = BOTTOM, expand = True, fill='x', anchor="w")

# resize button text size
# def resize(e):
#     print(window.winfo_reqwidth())
#     questions = tk.Label(pane1, bg="#f5f5f5", bd=4, relief=RAISED, text = qustion, font=('Digital-7', 14), wraplength=window.winfo_reqwidth(), background="#345", foreground = "white")
# window.bind('<Configure>', resize)

# window_width, window_height = 0, 0

scrollbar = Scrollbar(window)
editor = Text(yscrollcommand = scrollbar.set)
scrollbar.pack(side= RIGHT, fill= Y)
scrollbar.config(command= editor.yview)
editor.pack(fill= 'both', expand= True)


def newExam(event= 'n'):
    editor.delete(1.0,END)
    #TODO


def open(event= 'o'):
    showerror("open")
    #TODO

# quit Function.
def quit(event= 'q'):
    window.destroy
    # showerror("quit!!!")
    #TODO


def cutFile(event = 'x'):
    editor.event_generate("<<Cut>>")


def copyFile(event = 'c'):
    editor.event_generate("<<Copy>>")


def pasteFile(event = 'v'):
    editor.event_generate("<<Paste>>")


def Exit():
    window.quit()


def timesNewRoman():
    editor.configure(font=("times New Roman", 20, "italic"))
def Lucida():
    editor.configure(font=("lucida 25"))
def Algerian():
    editor.configure(font=("ALGERIAN", 20, "bold"))
def ARIAL():
    editor.configure(font=("Arial", 20, "bold"))
def Calibri():
    editor.configure(font=("Calibri", 20))
def Impact():
    editor.configure(font=("Impact", 20))
def modern():
    editor.configure(font=("Modern", 20))
def highTowerText():
    editor.configure(font=("High Tower Text", 20))
def Harrington():
    editor.configure(font=("Harrington", 20))


def font():
    window=Tk()
    window.title('FONT WINDOW')
    window.geometry('550x600')
    window.config(bg='#223441')
    window.resizable(width=False, height=False)

    lbl=Label(window,text="*****THIS IS FONT SELECTION PAGE*****",font=('times new roman',20), bg="#223441", fg="white")
    lbl.grid(column=0,row=0)
    lbl=Label(window,text='PLEASE SELECT THE FONT',font=('times new roman',20), bg="#223441", fg="white")
    lbl.grid(column=0,row=1, pady=10)
    btn=Button(window,text='Times new roman',command=timesNewRoman,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=3)
    btn=Button(window,text='lucida 20',command=Lucida, bg='white',font=('times new roman',20))
    btn.grid(column=0, row=4)
    btn=Button(window,text='ALGERIAN',command=Algerian,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=5)
    btn=Button(window,text='Arial',command=ARIAL,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=6)
    btn=Button(window,text='Calibri',command=Calibri,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=7)
    btn=Button(window,text='Impact',command=Impact,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=8)
    btn=Button(window,text='Modern',command=modern,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=9)
    btn=Button(window,text='High Tower Text',command=highTowerText,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=10)
    btn=Button(window,text='Harrington',command=Harrington,bg='white',font=('times new roman',20))
    btn.grid(column=0, row=11)

menubar = Menu(window, relief=RAISED)

filemenu=Menu(menubar,tearoff=0)
editmenu=Menu(menubar,tearoff=0)
formatmenu=Menu(menubar,tearoff=0)

menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label="New                 Ctrl+N", command=newExam)
filemenu.add_command(label="Open               Ctrl+O", command=open)
filemenu.add_command(label="cacel                 Ctrl+Q", command=quit)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=Exit)

menubar.add_cascade(label='Edit',menu=editmenu)
editmenu.add_cascade(label='Cut            Ctrl+X', command=cutFile)
editmenu.add_cascade(label='Copy         Ctrl+C', command=copyFile)
editmenu.add_cascade(label='Paste         Ctrl+V', command=pasteFile)

menubar.add_cascade(label='Format',menu=formatmenu)
formatmenu.add_cascade(label='Font', command=font)

window.config(menu=menubar)
# Shortcut Key bindings.
window.bind('<Control-n>', newExam)
window.bind('<Control-o>', open)
window.bind('<Control-q>', quit)
window.bind('<Control-x>', cutFile)
window.bind('<Control-c>', copyFile)
window.bind('<Control-v>', pasteFile)

# startCountdown()

window.after(1000, Update)
window.mainloop()