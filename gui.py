from datetime import datetime
from tkinter import *
from tkinter import Menu, messagebox, ttk

import language_tool_python

from database import (delete_exam, fetch_exams, fetch_matches, insert_exam, insert_match, number_of_suggestions)

tool = language_tool_python.LanguageTool("en-US")

ws = Tk()
ws.geometry("1100x300+410+200")
ws.title("Exams")
ws.config(bg="#223441")
ws.resizable(width=False, height=False)
# ws.wm_attributes("-topmost", 1)
# w/h (fill)
h1 = 5
w1 = 45
h2 = 5
w2 = 22
# pad
x1 = 5
y1 = 10
y1Top = 17
x2 = 5
y2 = 10


temp_exam_question_name = ""
temp_exam_question = ""
temp_exam_answer = ""
temp_date_time_created = ""
temp_date_time_finished = ""


def newEx():
    name = my_entry.get()
    if name != "" and len(text.get("1.0", "end-1c")) != 0:
        # save the exam name
        temp_exam_question_name = name
        # save the exam question
        temp_exam_question = text.get("1.0", "end-1c")
        # save start date/time of start of exam
        temp_date_time_created = datetime.now()
        # deleting entrys from GUI
        my_entry.delete(0, "end")
        text.delete(1.0, END)
        # delete list of exams
        lb.delete(0, "end")
        # hide main window
        hide()
        # save finished date/time of start of exam
        startExam(temp_exam_question_name, temp_exam_question, temp_date_time_created)
    else:
        messagebox.showwarning("warning", "Please enter Exam Name/Question.")


def updateList():
    for item in fetch_exams():
        st = item[6].split(" ")[0] + " (" + item[6].split(" ")[1].split(".")[0]
        try:
            ed = " - " + item[7].split(" ")[1].split(".")[0] + ")"
        except:
            ed = " - " + str(item[7]) + ")"
        lb.insert(END, (str(item[0]) + ") " + str(item[1]) + " - " + st + str(ed)))

    for item in range(len(fetch_exams())):
        lb.itemconfig(item, bg="#c7ecee" if item % 2 == 0 else "#95afc0")


def postExam(
    temp_exam_question_name,
    temp_exam_question,
    temp_exam_answer,
    temp_date_time_created,
    temp_date_time_finished,
):
    matches = tool.check(temp_exam_answer)
    miatakes_number = len(matches)
    autoCorrected = tool.correct(temp_exam_answer)

    exam = (
        temp_exam_question_name,
        temp_exam_question,
        miatakes_number,
        temp_exam_answer,
        autoCorrected,
        temp_date_time_created,
        temp_date_time_finished,
    )
    exam_id = insert_exam(exam)

    for match in matches:
        errText = match.message
        errOffset = match.offsetInContext
        errLength = match.errorLength
        context = match.context
        category = match.category
        ruleIssue = match.ruleIssueType
        sentence = match.sentence
        numberSuggestions = len(match.replacements)
        ruleID = match.ruleId
        Suggestions = match.replacements

        m = (
            errText,
            errOffset,
            errLength,
            context,
            category,
            ruleIssue,
            sentence,
            ruleID,
            numberSuggestions,
            str(Suggestions),
            exam_id,
        )

        insert_match(m)

    print("results in database.db!!!")
    tool.close()

def openSelected():
    reslist = list()
    seleccion = lb.curselection()
    for i in seleccion:
        entrada = lb.get(i)
        reslist.append(entrada)
    launch(reslist)


def deleteSelected():
    reslist = list()
    seleccion = lb.curselection()
    for j in seleccion:
        entrada = lb.get(j)
        lb.delete(j)
        reslist.append(entrada)
    for var in reslist:
        try:
            delete_exam(int(str(var).split(")")[0]))
        except:
            print()

def checkSuggestions(word):
    reslist = list()
    seleccion = lb.curselection()
    for j in seleccion:
        entrada = lb.get(j)
        reslist.append(entrada)
    for var in reslist:
        print(number_of_suggestions(int(str(var).split(")")[0]), word))
        lablFreq.configure(text= str(number_of_suggestions(int(str(var).split(")")[0], word))))
        # cal+=number_of_suggestions(int(str(var).split(")")[0], word))


# ---------------topPanel START-----------------
topPanel = Frame(ws, bg="#223441", bd=2)
topPanel.pack(side=TOP, fill="x", anchor="n")
# ---------------topPanel END-----------------

# ---------------openPanel START-----------------
openPanel = Frame(topPanel, bg="#223441", bd=2, relief="groove")
openPanel.pack(side=LEFT, fill=BOTH)

# TOP START
paneInputA = Frame(openPanel, bg="#223441")
paneInputA.pack(side=TOP, fill="x", padx=x2, pady=(y1Top, 0))

def print_selection():
    if (checkBox.get() == 1):
        my_word.config(state='normal')
        my_word.delete(0, "end")
    elif (checkBox.get() == 0):
        my_word.delete(0, "end")
        my_word.config(state='disabled')
    else:
        my_word.config(state='disabled')

# Define a Checkbox
checkBox = IntVar()
t1 = Checkbutton(paneInputA, bg="#223441", fg="#c7ecee", font=("times", 20), text="Search", variable=checkBox, onvalue=1, offvalue=0, command=print_selection)
t1.pack(side=LEFT, anchor="e")

lablFreq= Label(
    paneInputA,
    text="Mistakes",
    bg="#223441",
    fg="#c7ecee",
    font=("times", 20),
    borderwidth=2,
    relief="flat",
)
lablFreq.pack(side=LEFT, padx=(0, x2), anchor="e")

my_word = Entry(
    paneInputA,
    justify="left",
    font=("times", 20),
    bd=2,
    width=int(w1/1.5),
    relief="ridge",
    state='disabled'
)
my_word.pack(side=TOP, anchor="e")
# TOP END

# TOP START
topLPan = Frame(openPanel, bg="#223441")
topLPan.pack(side=TOP, fill="x", padx=x1, pady=(y1, 0))

lb = Listbox(
    topLPan,
    width=w1,
    height=h1,
    font=("Times", 20),
    bd=2,
    relief="ridge",
    fg="#464646",
    selectmode="multiple",
    highlightthickness=0,
    selectbackground="#a6a6a6",
    activestyle="none",
)
lb.pack(side=LEFT, fill=BOTH)

for item in fetch_exams():
    st = item[6].split(" ")[0] + " (" + item[6].split(" ")[1].split(".")[0]
    try:
        ed = " - " + item[7].split(" ")[1].split(".")[0] + ")"
    except:
        ed = " - " + str(item[7]) + ")"
    lb.insert(END, (str(item[0]) + ") " + str(item[1]) + " - " + st + str(ed)))

for item in range(len(fetch_exams())):
    lb.itemconfig(item, bg="#c7ecee" if item % 2 == 0 else "#95afc0")

sb = Scrollbar(topLPan)
sb.pack(side=LEFT, fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)
# TOP END

# BOTTOM START
btnPane = Frame(openPanel)
btnPane.pack(side=TOP, fill="x", padx=x1, pady=(0, y1))

open_btn = Button(
    btnPane,
    text="Open Exam",
    font=("times 14"),
    bg="#38ada9",
    padx=w1 / 2,
    pady=10,
    bd=2,
    relief=RAISED,
    command=openSelected,
)
open_btn.pack(fill="x", expand=True, side=RIGHT)

del_btn = Button(
    btnPane,
    text="Delete Exam",
    font=("times 14"),
    bg="#ff8b61",
    padx=w1 / 2,
    pady=10,
    bd=2,
    relief=RAISED,
    command=deleteSelected,
)
del_btn.pack(fill="x", expand=True, side=LEFT)
# BOTTOM END
# ---------------openPanel END-----------------

# ---------------enterPane START-----------------
enterPane = Frame(topPanel, bg="#223441", bd=2, relief="groove")
enterPane.pack(side=RIGHT, fill=BOTH)

# TOP START
paneInput = Frame(enterPane, bg="#223441")
paneInput.pack(side=TOP, fill="x", padx=x2, pady=(y2, 0))

Label(
    paneInput,
    text="Name     ",
    bg="#223441",
    fg="#c7ecee",
    font=("times", 20),
    borderwidth=2,
    relief="flat",
).pack(side=LEFT, padx=(0, x2))

my_entry = Entry(
    paneInput, width=w2, justify="left", font=("times", 20), bd=2, relief="ridge"
)
my_entry.pack(side=TOP, anchor="e")
# TOP END

# BOTTOM START
paneArea = Frame(enterPane, bg="#223441")
paneArea.pack(side=TOP, fill="x", padx=x2, pady=y2)

Label(
    paneArea,
    text="Question",
    bg="#223441",
    fg="#c7ecee",
    font=("times", 20),
    borderwidth=2,
    relief="flat",
).pack(side=LEFT, anchor="n", padx=(0, x2))

text = Text(
    paneArea,
    state=NORMAL,
    height=h2,
    width=w2,
    font=("times", 20),
    bd=2,
    relief="ridge",
)
text.pack()

# Button to add
button_frame = Frame(paneArea)
button_frame.pack(fill="x")

add_btn = Button(
    button_frame,
    text="Add Exam",
    font=("times 14"),
    bg="#c5f776",
    # padx=170,
    pady=10,
    bd=2,
    relief=RAISED,
    command=newEx,
)
add_btn.pack(fill=BOTH, expand=True, side=BOTTOM)
# BOTTOM END
# ---------------enterPane END-----------------

# ---------------midPanel START-----------------
# midPanel= Frame(ws, bg='#223441', bd=2, relief='groove')
# midPanel.pack(side=TOP, fill=BOTH)
# ---------------midPanel END-----------------

# ---------------mistakePane START-----------------
# mistakePane= Frame(midPanel, bg='#223441')
# mistakePane.pack(side=TOP, fill=BOTH)
# ---------------mistakePane END-----------------

# =====================================MISTAKE TABLE=====================================
def launch(obj):
    title= ""
    global mistakes
    mistakes = Toplevel(ws)
    mistakes.title("title")
    mistakes.geometry("1220x640")
    mistakes.config(bg="#223441")

    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", rowheight=40)
    s.configure("Treeview", font=("times", 14), rowheight=40)

    tree = ttk.Treeview(
        mistakes, column=("c1", "c2", "c3", "c4", "c5", "c6"), show="headings", height=15
    )

    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="ID")  # 0
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="ErrorText")  # 1
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="ruleIssue")  # 6
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="sentence")  # 7
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="numberSuggestions")  # 9
    tree.column("# 6", anchor=CENTER)
    tree.heading("# 6", text="Suggestions")  # 10

    for val in obj:
        title+= str(val).split(")")[1]
        i = 0

        for item in fetch_matches(int(str(val).split(")")[0])):
            i += 1
            if (checkBox.get() == 1 and int(item[9]) == 1 and str(item[10]).replace("['", "").replace("']","").strip().upper() == my_word.get().upper()):
                s= "sepecial"
            elif i % 2 == 0:
                s = "even"
            else:
                s = "odd"
            tree.insert(
                "",
                "end",
                text=i,
                values=(item[11], item[1], item[6], item[7], item[9], item[10]),
                tags=(s,),
            )

        tree.tag_configure("odd", background="#b8e994")
        tree.tag_configure("even", background="#38ada9")
        tree.tag_configure("sepecial", background="#ff5252")

    tree.pack()


# =====================================NEW EXAM=====================================
def startExam(temp_exam_question_name, temp_exam_question, temp_date_time_created):
    global window
    window = Toplevel(ws)
    try:
        window.title(
            temp_exam_question_name
            + " - ("
            + str(temp_date_time_created).split(" ")[1].split(".")[0]
            + ")"
        )
    except:
        print("err!!!")
    w = "900"
    h = "700"
    window.geometry(w + "x" + h)
    window.config(bg="#345")

    def stopdef():
        temp_exam_question_name
        temp_exam_question
        temp_date_time_created
        temp_date_time_finished = datetime.now()
        temp_exam_answer = text_box.get(1.0, "end-1c")
        postExam(
            temp_exam_question_name,
            temp_exam_question,
            temp_exam_answer,
            temp_date_time_created,
            temp_date_time_finished,
        )
        window.destroy()
        updateList()
        show()

    pane = Frame(window)
    pane.pack(fill="x", ipady=10)

    # date= date.today()
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    Time = Label(
        pane,
        text=f"{time}",
        background="black",
        foreground="red",
        font=("Digital-7", 20),
        relief=SOLID,
    )
    Time.pack(side=TOP, fill=BOTH, anchor="n", expand=True)

    def Update():
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        Time.config(text=f"{time}")
        Time.after(1000, Update)

    stop = Button(
        pane,
        text="Stop",
        font=("Digital-7", 20),
        bg="red",
        fg="white",
        relief="groove",
        command=stopdef,
    )
    stop.pack(side=LEFT, fill=BOTH, anchor="sw", expand=True)

    pane1 = Frame(pane, bg="#345")
    pane1.pack(side=RIGHT, fill=BOTH, anchor="e", expand=True)

    questions = Label(
        pane1,
        bg="#f5f5f5",
        bd=4,
        relief=RAISED,
        text=temp_exam_question,
        font=("Digital-7", 14),
        wraplength=w,
        height=5,
        background="#345",
        foreground="white",
        justify="left",
    )
    questions.place(relx=0.1, rely=0.5, relheight=0.4, relwidth=0.8)
    questions.pack(side=BOTTOM, expand=True, fill="x", anchor="w")

    # resize button text size
    def resize(e):
        questions.configure(wraplength=e.width)

    window.bind("<Configure>", resize)

    text_box = Text(
        window, height=h, width=w, font=("Digital-7", 14), relief=SUNKEN, bd=5
    )
    text_box.pack(fill=BOTH, expand=True)

    def cutFile(event="x"):
        text_box.event_generate("<<Cut>>")

    def copyFile(event="c"):
        text_box.event_generate("<<Copy>>")

    def pasteFile(event="v"):
        text_box.event_generate("<<Paste>>")

    def timesNewRoman():
        text_box.configure(font=("times New Roman", 20, "italic"))

    def Lucida():
        text_box.configure(font=("lucida 25"))

    def Algerian():
        text_box.configure(font=("ALGERIAN", 20, "bold"))

    def ARIAL():
        text_box.configure(font=("Arial", 20, "bold"))

    def Calibri():
        text_box.configure(font=("Calibri", 20))

    def Impact():
        text_box.configure(font=("Impact", 20))

    def modern():
        text_box.configure(font=("Modern", 20))

    def highTowerText():
        text_box.configure(font=("High Tower Text", 20))

    def Harrington():
        text_box.configure(font=("Harrington", 20))

    def font():
        window = Tk()
        window.title("FONT WINDOW")
        window.geometry("550x600")
        window.config(bg="#223441")
        window.resizable(width=False, height=False)

        lbl = Label(
            window,
            text="*****THIS IS FONT SELECTION PAGE*****",
            font=("times new roman", 20),
            bg="#223441",
            fg="white",
        )
        lbl.grid(column=0, row=0)
        lbl = Label(
            window,
            text="PLEASE SELECT THE FONT",
            font=("times new roman", 20),
            bg="#223441",
            fg="white",
        )
        lbl.grid(column=0, row=1, pady=10)
        btn = Button(
            window,
            text="Times new roman",
            command=timesNewRoman,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=3)
        btn = Button(
            window,
            text="lucida 20",
            command=Lucida,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=4)
        btn = Button(
            window,
            text="ALGERIAN",
            command=Algerian,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=5)
        btn = Button(
            window,
            text="Arial",
            command=ARIAL,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=6)
        btn = Button(
            window,
            text="Calibri",
            command=Calibri,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=7)
        btn = Button(
            window,
            text="Impact",
            command=Impact,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=8)
        btn = Button(
            window,
            text="Modern",
            command=modern,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=9)
        btn = Button(
            window,
            text="High Tower Text",
            command=highTowerText,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=10)
        btn = Button(
            window,
            text="Harrington",
            command=Harrington,
            bg="white",
            font=("times new roman", 20),
        )
        btn.grid(column=0, row=11)

    menubar = Menu(window, relief=RAISED)

    editmenu = Menu(menubar, tearoff=0)
    formatmenu = Menu(menubar, tearoff=0)

    menubar.add_cascade(label="Edit", menu=editmenu)
    editmenu.add_cascade(label="Cut            Ctrl+X", command=cutFile)
    editmenu.add_cascade(label="Copy         Ctrl+C", command=copyFile)
    editmenu.add_cascade(label="Paste         Ctrl+V", command=pasteFile)

    menubar.add_cascade(label="Format", menu=formatmenu)
    formatmenu.add_cascade(label="Font", command=font)

    window.config(menu=menubar)
    # Shortcut Key bindings.
    window.bind("<Control-x>", cutFile)
    window.bind("<Control-c>", copyFile)
    window.bind("<Control-v>", pasteFile)

    window.after(1000, Update)
    window.mainloop()


# Show the window
def show():
    ws.deiconify()


# Hide the window
def hide():
    ws.withdraw()


ws.mainloop()
