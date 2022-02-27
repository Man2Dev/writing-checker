import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys = 1")
cur = conn.cursor()

# Create 2 tables if they don't exist: Exams and Match
cur.execute(
    """CREATE TABLE IF NOT EXISTS Exams
(EID INTEGER PRIMARY KEY AUTOINCREMENT,
question_name VARCHAR,
question VARCHAR,
MistakesNumber INTEGER,
user_answer VARCHAR,
CorrectAnswer VARCHAR,
Created DATETIME DEFAULT CURRENT_TIMESTAMP,
finished DATETIME)"""
)

cur.execute(
    """CREATE TABLE IF NOT EXISTS Match
(ID INTEGER PRIMARY KEY AUTOINCREMENT,
ErrorText VARCHAR,
ErrorOffset INTEGER,
ErrorLength INTEGER,
Context VARCHAR,
Category VARCHAR,
ruleIssue VARCHAR,
sentence VARCHAR,
ruleID VARCHAR,
numberSuggestions INTEGER,
Suggestions VARCHAR,
EID             INT,
FOREIGN KEY (EID) REFERENCES Exams (EID))"""
)

conn.commit()

# create an instance of Exams table
def insert_exam(entities):
    cur.execute(
        "INSERT INTO Exams(question_name, question, MistakesNumber, user_answer, CorrectAnswer, Created, finished) VALUES(?, ?, ?, ?, ?, ?, ?)",
        entities,
    )
    conn.commit()


# return a list of user's exams
def fetch_exams():
    cur.execute("SELECT * FROM Exams")
    rows = cur.fetchall()

    exams = list()
    for row in rows:
        exams.append(row)

    return exams


# create an instance of Match table
def insert_match(entities):
    cur.execute(
        "INSERT INTO Match(ErrorText, ErrorOffset, ErrorLength, Context, Category, ruleIssue, sentence, ruleID, numberSuggestions, Suggestions, EID) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        entities,
    )
    conn.commit()


# delete a match by its id
def delete_match(pk):
    cur.execute("DELETE FROM Match WHERE id= " + str(pk))
    conn.commit()


# return a list of the matches of a specific exam using ExamID (foreign key)
def fetch_matches(fk):
    cur.execute("SELECT * FROM Match WHERE EID = " + str(fk))
    rows = cur.fetchall()

    matches = list()
    for row in rows:
        matches.append(row)

    return matches


# example...
exam = (
    "first question",
    "what is your name child?",
    5,
    "I'm hendiani! the guz master!",
    "there is no correct answer!",
    1400,
    1400,
)
insert_exam(exam)

match = ("error text", 3, 4, "dddd", "aa", "ss", "dd", "dd", 3, "sd", 1)
insert_match(match)

# delete_match(1)

print(fetch_exams())
print("\n")
print(fetch_matches(1))
