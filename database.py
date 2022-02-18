import sqlite3

# con = sqlite3.connect("database.db")
conn.execute("PRAGMA foreign_keys = 1")
# cursor = con.cursor()

# cursor.executescript(
#     """CREATE TABLE IF NOT EXISTS exams
#     (
#         ExamID INTEGER not null
#             primary key autoincrement,
#         image BLOB,
#         MistakesNumber INTEGER,
#         inputText VARCHAR,
#         CorrectAnswer VARCHAR,
#         Created INTEGER,
#         finished INTEGER
#     );
#     """
# )

# cursor.executescript(
#     """CREATE TABLE IF NOT EXISTS match
#     (
#         id INTEGER not null
#             primary key autoincrement,
#         ErrorText VARCHAR,
#         ErrorOffset INTEGER,
#         ErrorLength INTEGER
#         Context VARCHAR,
#         Category VARCHAR,
#         ruleIssue VARCHAR,
#         sentence VARCHAR,
#         ruleID VARCHAR,
#         numberSuggestions INTEGER,
#         Suggestions VARCHAR,
#         FOREIGN KEY(ExamID) REFERENCES exams(ExamID))
#     );
#     """
# )

# # def add_exam(
# #     ErrorText, ErrorOffset, ErrorLength, image,
# #     Context, Category, ruleIssue, sentence,
# #     ruleID, numberSuggestions, Suggestions, MistakesNumber,
# #     inputText, CorrectAnswer, Created, finished,
# # ):

# #     cursor.execute(
# #         """INSERT INTO exams (ErrorText, ErrorOffset, ErrorLength, image, Context,
# #         Category, ruleIssue, sentence, ruleID, numberSuggestions, Suggestions,
# #         MistakesNumber, inputText, CorrectAnswer, Created, finished) 
# #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
# #         (
# #             ErrorText,
# #             ErrorOffset,
# #             ErrorLength,
# #             image,
# #             Context,
# #             Category,
# #             ruleIssue,
# #             sentence,
# #             ruleID,
# #             numberSuggestions,
# #             Suggestions,
# #             MistakesNumber,
# #             inputText,
# #             CorrectAnswer,
# #             Created,
# #             finished,
# #         ),
# #     )
# #     con.commit()



conn=sqlite3.connect("clientdatabase.db")
conn.execute("PRAGMA foreign_keys = 1")
cur=conn.cursor()

# Create 2 tables if they don't exist: Clients and Work_Done
cur.execute('''CREATE TABLE IF NOT EXISTS Clients
(CID INTEGER PRIMARY KEY,
First_Name  TEXT    NOT NULL,
Last_Name       TEXT,
Business_Name   TEXT,
Phone           TEXT,
Address         TEXT,
City            TEXT,
Notes           TEXT,
Active_Status   TEXT    NOT NULL)''')      

cur.execute('''CREATE TABLE IF NOT EXISTS Work_Done
(ID INTEGER PRIMARY KEY,
Date            TEXT    NOT NULL,
Onsite_Contact  TEXT,
Work_Done       TEXT    NOT NULL,
Parts_Installed TEXT,
Next_Steps      TEXT,
CID             INT,
FOREIGN KEY (CID) REFERENCES CLIENTS (CID))''')
conn.commit()