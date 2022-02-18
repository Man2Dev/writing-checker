import sqlite3
#from main import

con = sqlite3.connect('mistakes.db')

c = con.cursor()

c.execute("""CREATE TABLE data (
            first text,
            last text,
            pay integer
            )""")

def new_user_operator(chat_id, first_name, username, phone_number,is_operator):
    cursor.execute("""INSERT INTO operator (chat_id, first_name, username, phone_number, is_making_order, is_operator,
     is_administrator) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, first_name, username, phone_number, 0, 1, 0))
    conn.commit()
