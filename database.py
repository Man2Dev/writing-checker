import sqlite3

# from main import

con = sqlite3.connect("database.db")

cursor = con.cursor()

cursor.executescript(
    """CREATE TABLE IF NOT EXISTS exams
    (
        id INTEGER not null
            primary key autoincrement,
        ErrorText VARCHAR,
        ErrorOffset INTEGER,
        ErrorLength INTEGER
        image BLOB,
        Context VARCHAR,
        Category VARCHAR,
        ruleIssue VARCHAR,
        sentence VARCHAR,
        ruleID VARCHAR,
        numberSuggestions INTEGER,
        Suggestions VARCHAR,
        MistakesNumber INTEGER,
        inputText VARCHAR,
        CorrectAnswer VARCHAR,
        Created INTEGER,
        finished INTEGER
    );
    """
)


def add_exam(
    ErrorText, ErrorOffset, ErrorLength, image,
    Context, Category, ruleIssue, sentence,
    ruleID, numberSuggestions, Suggestions, MistakesNumber,
    inputText, CorrectAnswer, Created, finished,
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
