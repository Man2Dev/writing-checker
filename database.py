import sqlite3
#from main import

con = sqlite3.connect('database.db')

cursor = con.cursor()

cursor.executescript("""CREATE TABLE IF NOT EXISTS products
    (
        id INTEGER not null
            primary key autoincrement,
        ErrorText VARCHAR,
        ErrorOffset INTEGER,
        ErrorLength INTEGER
        image BLOB,
        Context VARCHAR,
        Category VARCHAR,
        RuleIssue VARCHAR,
        sentence VARCHAR,
        ContinuenumberSuggestions INTEGER
        Suggestions VARCHAR

        bot_shows BOOLEAN
    );
    """)