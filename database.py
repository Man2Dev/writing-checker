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
FOREIGN KEY (EID) REFERENCES Exams (EID))"""
)

conn.commit()


# create an instance of Exams table and return its id
def insert_exam(entities):
    cur.execute(
        "INSERT INTO Exams(question_name, question, MistakesNumber, user_answer, CorrectAnswer, Created) VALUES(?, ?, ?, ?, ?, ?)",
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
# exam = (
#     "first question",
#     "what is your name child?",
#     5,
#     "I'm hendiani! the guz master!",
#     "there is no correct answer!",
#     1400,
#     1400,
# )
# insert_exam(exam)

# match = ("error text", 3, 4, "dddd", "aa", "ss", "dd", "dd", 3, "sd", 1)
# insert_match(match)

# delete_match(1)

# print(fetch_exams())
# print("\n")
# print(fetch_matches(1))

answer = """The world today uses more renewable energy than ever before since it contributes to the preservation of the environment and is economically sound; however, some argue that green energy could undermine the reliability of the global supply as a result of its dependency on climatic and meteorological phenomena. This essay will examine both views, but personally, I strongly advocate the adoption of renewable sources of energy.

On the one hand, opponents of renewables claim that the world could face disruptions to the power supply should they be fully adopted. This is largely due to the fact that many green energy technologies currently in use depend on changeable and unpredictable phenomena such as wind, rain and cloud cover.

To take the fastest growing sector as an example, solar panels can only be used in the presence of strong and direct sunlight, and although the problem of directness has already been somewhat solved with moving panel arrays, a cloudy few days could still result in a blackout if we depended entirely on solar power; something that is unlikely to occur today given current oil stockpiles.

However, fossil fuels are a larger threat to energy security since they are certainly finite in quantity, whereas renewable energy is effectively infinite; once the Earth’s oil is depleted, there will be no energy security without green energy technologies.

Furthermore, problems of unpredictability can be mitigated by improving battery technologies (to create a larger buffer), building more renewable energy generators (to increase supply during ideal conditions) and improving current technologies (to increase efficiency), such as in the moving solar panel example. Proponents of renewables therefore claim that they are the most economically sound option.

To conclude, while many may believe that green energy technologies are a threat to energy security, the fossil fuels they frequently promote are a greater threat, and renewables are in fact the only sound option, both economically and environmentally."""


question = """Nowadays most green energy is becoming evermore prevalent in both developed and developing countries. Some argue they greatly reduce costs and are better for the environment, others believe they are a serious threat to energy security. Discuss both views and give your opinion."""
