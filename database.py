import sqlite3

conn=sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys = 1")
cur=conn.cursor()

# Create 2 tables if they don't exist: Exams and Match
cur.execute('''CREATE TABLE IF NOT EXISTS Exams
(EID INTEGER PRIMARY KEY,
image BLOB,
MistakesNumber INTEGER,
inputText VARCHAR,
CorrectAnswer VARCHAR,
Created TEXT,
finished TEXT)''')      

cur.execute('''CREATE TABLE IF NOT EXISTS Match
(ID INTEGER PRIMARY KEY,
ErrorText VARCHAR,
ErrorOffset INTEGER,
ErrorLength INTEGER
Context VARCHAR,
Category VARCHAR,
ruleIssue VARCHAR,
sentence VARCHAR,
ruleID VARCHAR,
numberSuggestions INTEGER,
Suggestions VARCHAR,
EID             INT,
FOREIGN KEY (EID) REFERENCES Exams (EID))''')

conn.commit()