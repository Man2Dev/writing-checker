import sqlite3
#from main import

con = sqlite3.connect('mistakes.db')

c = con.cursor()

c.execute("""CREATE TABLE data (
            first text,
            last text,
            pay integer
            )""")