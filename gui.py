from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Text
from tkinter import ttk
from database import fetch_exams
from database import fetch_matches
from datetime import datetime

question_name= ""
exam_question= ""
exam_answer=  ""
created_date= datetime.now()
# end_date= datetime.now()
te=int(len(fetch_exams()))

def newEx():
    name= my_entry.get()
    if name != "" and len(text.get("1.0", "end-1c")) != 0:
        # te=
        # te+=1
        globals()['te']= te+1
        item= str(te)+") "+ name+" - "+str(datetime.now()).split(" ")[0]+" ("+str(datetime.now()).split(" ")[1].split(".")[0]+" - None)"
        lb.insert(END, item)
        for item in range(te):
            lb.itemconfig(item, bg= "#c7ecee" if item % 2 == 0 else "#95afc0")
        question_name= name+" - "+str(datetime.now()).split(" ")[0]+" ("+str(datetime.now()).split(" ")[1].split(".")[0]+" - NOW)"
        exam_question= text.get("1.0", "end-1c")
        created_date= datetime.now()
        # launchEssay(question_name, exam_question, created_date)
        my_entry.delete(0, "end")
        text.delete(1.0,END)
    else:
        messagebox.showwarning("warning", "Please enter Exam Name/Question.")


# def delEx():
#     # TODO
#     # if int(str(lb.curselection()).split("(")[1].split(",")[0]) == 0:
#     #     lb.delete(0,END)
#     # else:
#     #     lb.delete(ANCHOR)
#     reslist= list()
#     seleccion= lb.curselection()
#     for i in seleccion:
#         entrada= lb.get(i)
#         reslist.append(entrada)
#     for val in reslist:
#         lb.delete(ANCHOR)


# def showSelected():
#     # TODO
#     value= lb.get(lb.curselection())
#     print(value)


def select():
    reslist= list()
    seleccion= lb.curselection()
    for i in seleccion:
        entrada= lb.get(i)
        reslist.append(entrada)
    for val in reslist:
        # mistakeTable(int(str(val).split(")")[0]))
        launch(int(str(val).split(")")[0]), str(val).split(")")[1]+")")


def delSelect():
    # tmp= list()
    for i in lb.curselection()[::-1]:
        # tmp.append(lb.get(i))
        lb.delete(i)
    for item in range(te-len(lb.curselection())):
        lb.itemconfig(item, bg= "#c7ecee" if item % 2 == 0 else "#95afc0")


ws= Tk()
ws.geometry('1000x250+500+200')

ws.title('Exams')
ws.config(bg='#223441')
# ws.resizable(width=False, height=False)
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

# lb.insert(END, "All exams")
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
    command=select
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
    command=delSelect
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
midPanel= Frame(ws, bg='#223441', bd=2, relief='groove')
midPanel.pack(side=TOP, fill=BOTH)
#---------------midPanel END-----------------

#---------------mistakePane START-----------------
mistakePane= Frame(midPanel, bg='#223441')
mistakePane.pack(side=TOP, fill=BOTH)

#---------------mistakePane END-----------------
def launch(id, t):
    global second
    second= Toplevel()
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

# Show the window
def show():
    second.deiconify()

# Hide the window
def hide():
    second.withdraw()


# def launchEssay(title, qustion, now):
#     global third
#     third= Toplevel()
#     third.title(title)
#     third.geometry("1220x640")
#     third.config(bg='#223441')

#     topPane= Frame(third)
#     topPane.pack(side=TOP, fill= BOTH, bg='#223441', bd=2, relief='groove', ipady=10)

#     topRightPane= Frame(topPane)
#     topRightPane.pack(side=RIGHT, fill= "x", bg='#223441', bd=2, relief='groove', ipady=10)

#     RightPaneStack= Frame(topRightPane)
#     RightPaneStack.pack(side=RIGHT, fill= "x", bg='#223441', bd=2, relief='groove', ipady=10)



#     stop= Button(RightPaneStack, text= "Stop", background= "red", fg= "white", font=('Digital-7', 20), relief=GROOVE)
#     stop.pack(side= BOTTOM, fill=BOTH, expand= True)

#     topLeftPane= Frame(topPane)
#     topLeftPane.pack(side=LEFT, fill= "x", bg='#223441', bd=2, relief='groove', ipady=10)

#     questionPan= Frame(topLeftPane, bg="#345")
#     questionPan.pack(fill= BOTH, expand= True)

#     questions= Label(questionPan, bg="#f5f5f5", bd=4, relief=RAISED, text= qustion, font=('Digital-7', 20), wraplength=700, background="#345", foreground= "white")
#     questions.place(relx=0.1, rely=0.5, relheight=0.4, relwidth=0.8)
#     questions.pack(side= BOTTOM, expand= True, fill= 'both', anchor="w")

#     topPane.after(1000, Update)
ws.mainloop()