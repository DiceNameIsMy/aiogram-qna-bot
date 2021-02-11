import sqlite3

connection = sqlite3.connect("UserData.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS questions
    (_id INTEGER PRIMARY KEY,
     author_id VARCHAR(9),
     question VARCHAR(256),
     best_answer_id INTEGER)
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS answers
    (_id INTEGER PRIMARY KEY,
    author_id VARCHAR(9),
    question_id INTEGER,
    answer VARCHAR(256))
""")    


connection.commit()
connection.close()
