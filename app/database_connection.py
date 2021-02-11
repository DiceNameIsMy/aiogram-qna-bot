import random

import sqlite3

connection = sqlite3.connect("mainData.db")
cursor = connection.cursor()


def insert_question(user_id, text):
    model = (user_id, text)
    cursor.execute("INSERT INTO questions(author, question) VALUES(?, ?)", model)
    print(user_id)
    print(text)
    connection.commit()


def return_questions(user_id):
    cursor.execute(f"SELECT * FROM questions WHERE author LIKE '{user_id}'")
    data = cursor.fetchall()
    questions = ''

    for i in range(len(data)):
        questions += f'{data[i][0]}. {data[i][2]}\n'

    return questions


def ask_question():
    cursor.execute("SELECT COUNT(*) FROM questions")
    x = int(cursor.fetchone()[0])
    cursor.execute(f"SELECT id, question FROM questions WHERE id LIKE '{random.randint(1,x+1)}' ")

    # question = cursor.fetchone()
    return cursor.fetchone()


def insert_answer(question_id, answer):
    model = (question_id, answer)
    cursor.execute("INSERT INTO answers(id_question, answer) VALUES(?, ?)", model)
    connection.commit()
