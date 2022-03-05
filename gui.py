from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import Menu
from datetime import datetime
import language_tool_python
from database import fetch_exams
from database import fetch_matches
from database import insert_exam, insert_match
tool= language_tool_python.LanguageTool("en-US")


ws= Tk()
ws.geometry('1000x250+500+200')
ws.title('Exams')
ws.config(bg='#223441')
ws.resizable(width=False, height=False)
# w/h (fill)
h1=5
w1=40
h2=4
w2=22
# pad
x1=5
y1=10
y1Top=17
x2=5
y2=10


temp_exam_question_name= ""
temp_exam_question= ""
temp_exam_answer= ""
temp_date_time_created= ""
temp_date_time_finished= ""

global realCount
realCount= len(fetch_exams())

def newEx():
    name= my_entry.get()
    if name != "" and len(text.get("1.0", "end-1c")) != 0:
        globals()['realCount']+= 1
        # save the exam name
        temp_exam_question_name= name
        # save the exam question
        temp_exam_question= text.get("1.0", "end-1c")
        # save start date/time of start of exam
        temp_date_time_created= datetime.now()
        # deleting entrys from GUI
        my_entry.delete(0, "end")
        text.delete(1.0,END)
        # delete list of exams
        lb.delete(0,'end')
        # hide main window
        hide()
        # save finished date/time of start of exam
        startExam(temp_exam_question_name, temp_exam_question, temp_date_time_created)
    else:
        messagebox.showwarning("warning", "Please enter Exam Name/Question.")

def updateList():
    for item in fetch_exams():
        st= item[6].split(" ")[0]+" ("+item[6].split(" ")[1].split(".")[0]
        try:
            ed= " - "+item[7].split(" ")[1].split(".")[0]+")"
        except:
            ed= " - "+str(item[7])+")"
        lb.insert(END, (str(item[0])+") "+str(item[1])+" - "+st+str(ed)))

    for item in range(len(fetch_exams())):
        lb.itemconfig(item, bg= "#c7ecee" if item % 2 == 0 else "#95afc0")


def postExam(temp_exam_question_name, temp_exam_question, temp_exam_answer, temp_date_time_created, temp_date_time_finished):
    matches= tool.check(temp_exam_answer)
    miatakes_number= len(matches)
    autoCorrected= tool.correct(temp_exam_answer)

    exam= (temp_exam_question_name, temp_exam_question, miatakes_number, temp_exam_answer, autoCorrected, temp_date_time_created, temp_date_time_finished)
    exam_id= insert_exam(exam)


    for match in matches:
        errText= match.message
        errOffset= match.offsetInContext
        errLength= match.errorLength
        context= match.context
        category= match.category
        ruleIssue= match.ruleIssueType
        sentence= match.sentence
        numberSuggestions= len(match.replacements)
        ruleID= match.ruleId
        Suggestions= match.replacements

        m= (
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
    reslist= list()
    seleccion= lb.curselection()
    for i in seleccion:
        entrada= lb.get(i)
        reslist.append(entrada)
    for val in reslist:
        launch(int(str(val).split(")")[0]), str(val).split(")")[1]+")")


def deleteSelected():
    globals()['realCount']-=len(lb.curselection())
    tmp= list()
    for i in lb.curselection()[::-1]:
        tmp.append(lb.get(i))
        lb.delete(i)
    for item in range(int(realCount)):
        lb.itemconfig(item, bg= "#c7ecee" if item % 2 == 0 else "#95afc0")


#---------------topPanel START-----------------
topPanel= Frame(ws, bg='#223441', bd=2)
topPanel.pack(side=TOP, fill='x', anchor='n')
#---------------topPanel END-----------------

#---------------openPanel START-----------------
openPanel= Frame(topPanel, bg='#223441', bd=2, relief='groove')
openPanel.pack(side=LEFT, fill=BOTH)

# TOP START
topLPan= Frame(openPanel, bg='#223441')
topLPan.pack(side=TOP, fill='x', padx=x1, pady=(y1Top, 0))

lb= Listbox(
    topLPan,
    width=w1,
    height=h1,
    font=('Times', 20),
    bd=2,
    relief='ridge',
    fg='#464646',
    selectmode= "multiple",
    highlightthickness=0,
    selectbackground='#a6a6a6',
    activestyle="none",
)
lb.pack(side=LEFT, fill=BOTH)

for item in fetch_exams():
    st= item[6].split(" ")[0]+" ("+item[6].split(" ")[1].split(".")[0]
    try:
        ed= " - "+item[7].split(" ")[1].split(".")[0]+")"
    except:
        ed= " - "+str(item[7])+")"
    lb.insert(END, (str(item[0])+") "+str(item[1])+" - "+st+str(ed)))

for item in range(len(fetch_exams())):
    lb.itemconfig(item, bg= "#c7ecee" if item % 2 == 0 else "#95afc0")

sb= Scrollbar(topLPan)
sb.pack(side=LEFT, fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)
# TOP END

# BOTTOM START
btnPane= Frame(openPanel)
btnPane.pack(side=TOP, fill='x', padx=x1, pady=(0, y1))

open_btn= Button(
    btnPane,
    text='Open Exam',
    font=('times 14'),
    bg='#38ada9',
    padx=w1/2,
    pady=10,
    bd=2,
    relief=RAISED,
    command=openSelected
)
open_btn.pack(fill='x', expand=True, side=RIGHT)

del_btn= Button(
    btnPane,
    text='Delete Exam',
    font=('times 14'),
    bg='#ff8b61',
    padx=w1/2,
    pady=10,
    bd=2,
    relief=RAISED,
    command=deleteSelected
)
del_btn.pack(fill='x', expand=True, side=LEFT)
# BOTTOM END
#---------------openPanel END-----------------

#---------------enterPane START-----------------
enterPane= Frame(topPanel, bg='#223441', bd=2, relief='groove')
enterPane.pack(side=RIGHT, fill=BOTH)

# TOP START
paneInput= Frame(enterPane, bg='#223441')
paneInput.pack(side=TOP, fill='x', padx=x2, pady=(y2, 0))

Label(paneInput, text="Name     ", bg='#223441', fg='#c7ecee', font=('times', 20), borderwidth=2, relief="flat").pack(side=LEFT, padx=(0, x2))
my_entry= Entry(paneInput, width=w2, justify='left', font=('times', 20), bd=2, relief='ridge')
my_entry.pack(side=TOP, anchor='e')
# TOP END

# BOTTOM START
paneArea= Frame(enterPane, bg='#223441')
paneArea.pack(side=TOP, fill='x', padx=x2, pady=y2)

Label(paneArea, text="Question", bg='#223441', fg='#c7ecee', font=('times', 20), borderwidth=2, relief="flat").pack(side=LEFT, anchor='n', padx=(0, x2))
text= Text(paneArea, state=NORMAL, height=h2, width=w2, font=('times', 20), bd=2, relief='ridge')
text.pack()

# Button to add
button_frame= Frame(paneArea)
button_frame.pack(fill='x')

add_btn= Button(
    button_frame,
    text='Add Exam',
    font=('times 14'),
    bg='#c5f776',
    # padx=170,
    pady=10,
    bd=2,
    relief=RAISED,
    command=newEx
)
add_btn.pack(fill=BOTH, expand=True, side=BOTTOM)
# BOTTOM END
#---------------enterPane END-----------------

#---------------midPanel START-----------------
# midPanel= Frame(ws, bg='#223441', bd=2, relief='groove')
# midPanel.pack(side=TOP, fill=BOTH)
#---------------midPanel END-----------------

#---------------mistakePane START-----------------
# mistakePane= Frame(midPanel, bg='#223441')
# mistakePane.pack(side=TOP, fill=BOTH)

#---------------mistakePane END-----------------

# =====================================MISTAKE TABLE=====================================
def launch(id, t):
    global second
    second= Toplevel(ws)
    second.title(t)
    second.geometry("1220x640")
    second.config(bg='#223441')

    s= ttk.Style()
    s.theme_use('clam')
    s.configure("Treeview", rowheight=40)
    s.configure("Treeview", font=('times', 14), rowheight=40)

    tree= ttk.Treeview(second, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=15)

    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="ID")#0
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="ErrorText")#1
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="ruleIssue")#6
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="sentence")#7
    tree.column("# 5", anchor=CENTER)
    tree.heading("# 5", text="numberSuggestions")#9
    tree.column("# 6", anchor=CENTER)
    tree.heading("# 6", text="Suggestions")#10

    # Insert the data in Treeview widget
    i=0
    # id=9
    for item in fetch_matches(id):
        i+=1
        if i%2==0:
            s='even'
        else:
            s='odd'

        tree.insert('', 'end', text=i, values=(item[0], item[1], item[6], item[7], item[9], item[10]),tags= (s,))

    tree.tag_configure('odd', background='#b8e994')
    tree.tag_configure('even', background='#38ada9')

    tree.pack()

# =====================================NEW EXAM=====================================
def startExam(temp_exam_question_name, temp_exam_question, temp_date_time_created):
    global window
    window=Toplevel(ws)
    try:
        window.title(temp_exam_question_name+" - ("+str(temp_date_time_created).split(" ")[1].split(".")[0]+")")
    except:
        print("err!!!")
    w= "700"
    h= "600"
    window.geometry(w+"x"+h)
    window.config(bg='#345')


    def stopdef():
        temp_exam_question_name
        temp_exam_question
        temp_date_time_created
        temp_date_time_finished= datetime.now()
        temp_exam_answer= text_box.get(1.0, "end-1c")
        postExam(temp_exam_question_name, temp_exam_question, temp_exam_answer, temp_date_time_created, temp_date_time_finished)
        window.destroy()
        updateList()
        show()


    pane= Frame(window)
    pane.pack(fill= 'x', ipady=10)

    # date= date.today()
    now= datetime.now()
    time= now.strftime("%H:%M:%S")

    Time= Label(pane, text= f"{time}", background="black", foreground= "red", font=('Digital-7', 20), relief=SOLID)
    Time.pack(side= LEFT, fill= BOTH, anchor='nw', expand= True)

    def Update():
        now= datetime.now()
        time= now.strftime("%H:%M:%S")
        Time.config(text= f"{time}")
        Time.after(1000, Update)

    stop= Button(pane, text='Stop', font=('Digital-7', 20), bg='red', fg='white', relief='groove', command=stopdef)
    stop.pack(side= LEFT, fill= BOTH, anchor='sw', expand= True)

    pane1= Frame(pane, bg="#345")
    pane1.pack(side= RIGHT, fill= BOTH, anchor='e', expand= True)

    questions= Label(pane1, bg="#f5f5f5", bd=4, relief=RAISED, text= temp_exam_question, font=('Digital-7', 14), wraplength=w, height=5, background="#345", foreground= "white", justify='left')
    questions.place(relx=0.1, rely=0.5, relheight=0.4, relwidth=0.8)
    questions.pack(side= BOTTOM, expand= True, fill='x', anchor="w")

    # resize button text size
    def resize(e):
        questions.configure(wraplength=e.width)
    window.bind('<Configure>', resize)

    text_box = Text(
        window,
        height=h,
        width=w,
        font=('Digital-7', 14),
        relief=SUNKEN,
        bd=5
    )
    text_box.pack(fill= BOTH, expand=True)


    def cutFile(event= 'x'):
        text_box.event_generate("<<Cut>>")


    def copyFile(event= 'c'):
        text_box.event_generate("<<Copy>>")


    def pasteFile(event= 'v'):
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

    menubar= Menu(window, relief=RAISED)

    editmenu=Menu(menubar,tearoff=0)
    formatmenu=Menu(menubar,tearoff=0)

    menubar.add_cascade(label='Edit',menu=editmenu)
    editmenu.add_cascade(label='Cut            Ctrl+X', command=cutFile)
    editmenu.add_cascade(label='Copy         Ctrl+C', command=copyFile)
    editmenu.add_cascade(label='Paste         Ctrl+V', command=pasteFile)

    menubar.add_cascade(label='Format',menu=formatmenu)
    formatmenu.add_cascade(label='Font', command=font)

    window.config(menu=menubar)
    # Shortcut Key bindings.
    window.bind('<Control-x>', cutFile)
    window.bind('<Control-c>', copyFile)
    window.bind('<Control-v>', pasteFile)

    window.after(1000, Update)
    window.mainloop()

# Show the window
def show():
    ws.deiconify()

# Hide the window
def hide():
    ws.withdraw()

ws.mainloop()