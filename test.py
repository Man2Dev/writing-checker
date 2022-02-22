import sqlite3

con = sqlite3.connect("database.db")
con.execute("PRAGMA foreign_keys = 1")
cursor = con.cursor()

cursor.executescript(
    """CREATE TABLE IF NOT EXISTS exams (
        ID INTEGER PRIMARY KEY,
        image BLOB,
        MistakesNumber INTEGER,
        inputText VARCHAR,
        CorrectAnswer VARCHAR,
        Created INTEGER,
        finished INTEGER
    );
    """
)


cursor.executescript(
    """CREATE TABLE IF NOT EXISTS match
    (
       ID INTEGER PRIMARY KEY,
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
        family_id INTEGER,
        FOREIGN KEY(family_id) REFERENCES families(ID)
    );
    """
)


def add_exam(
    ErrorText,
    ErrorOffset,
    ErrorLength,
    image,
    Context,
    Category,
    ruleIssue,
    sentence,
    ruleID,
    numberSuggestions,
    Suggestions,
    MistakesNumber,
    inputText,
    CorrectAnswer,
    Created,
    finished,
):

    cursor.execute(
        """INSERT INTO exams (ErrorText, ErrorOffset, ErrorLength, image, Context,
        Category, ruleIssue, sentence, ruleID, numberSuggestions, Suggestions,
        MistakesNumber, inputText, CorrectAnswer, Created, finished)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            ErrorText,
            ErrorOffset,
            ErrorLength,
            image,
            Context,
            Category,
            ruleIssue,
            sentence,
            ruleID,
            numberSuggestions,
            Suggestions,
            MistakesNumber,
            inputText,
            CorrectAnswer,
            Created,
            finished,
        ),
    )
    con.commit()
