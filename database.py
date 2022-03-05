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
finished DATETIME DEFAULT NULL)"""
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

CONSTRAINT fk_exam
FOREIGN KEY (EID) REFERENCES Exams (EID)
ON DELETE CASCADE)
"""
)

conn.commit()


# create an instance of Exams table and return its id
def insert_exam(entities):
    cur.execute(
        "INSERT INTO Exams(question_name, question, MistakesNumber, user_answer, CorrectAnswer, Created, finished) VALUES(?, ?, ?, ?, ?, ?, ?)",
        entities,
    )
    conn.commit()

    return cur.lastrowid


# return a list of user's exams
def fetch_exams():
    cur.execute("SELECT * FROM Exams")
    rows = cur.fetchall()

    exams = list()
    for row in rows:
        exams.append(row)

    return exams


# delete a Exam by its id
def delete_exam(pk):
    cur.execute("DELETE FROM Exams WHERE EID= " + str(pk))

    # matches = fetch_matches(pk)
    # for match in matches:
    #     delete_match(match.id)

    conn.commit()


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


# return a list of the matches of a specific exam using EID
def fetch_matches(fk):
    cur.execute("SELECT * FROM Match WHERE EID = " + str(fk))
    rows = cur.fetchall()

    matches = list()
    for row in rows:
        matches.append(row)

    return matches


# return number of occurence of a word in the selected exam
def number_of_suggestions(exam_id, word):
    cur.execute(f"SELECT Suggestions FROM Match WHERE EID = '{exam_id}' AND Suggestions LIKE '%{word}%' AND numberSuggestions = 1")
    rows = cur.fetchall()
    return len(rows)


# return a dictionary of each ruleIssue and number of its occurence
def number_of_ruleIssues(exam_id):
    cur.execute(f"SELECT ruleIssue, COUNT(*) as COUNT from Match GROUP BY ruleIssue")
    rows = cur.fetchall()
    return dict(rows)


# d = {'misspelling': 2, 'typographical': 1}

# print(d['misspelling'])
