from flask import Flask
from datetime import date
import database_connection as dc
import random

# Function that takes a list of selected tags and returns query results
def queryQuestions(cursor, selected_tags):

    # This is the list of equal statements for the database
    equal_statement = []

    # Fill list with equal statements
    for tag in selected_tags:
        equal_statement.append(f"t.tag_name = '{tag}'")

    # Add 'or' inbetween equal statements
    or_statement = " or ".join(equal_statement)

    
    query_top = """SELECT q.question_ID
         FROM question q
         JOIN tag_question tq ON tq.question_ID = q.question_ID
         JOIN tag t on t.tag_ID = tq.tag_ID """
    query_middle = "WHERE ("
    query_bottom = "GROUP BY q.question_ID"

    # Add the equal statements to middle query
    query_middle += or_statement
    query_middle += ") AND q.is_active = 1 " # only get active questions

    cursor.execute(query_top + query_middle + query_bottom)

    return cursor.fetchall()

def makeTest(cnx, select_tags, num_questions, users_id, name, is_tutor_mode, is_time_mode, date):
    
    cursor = cnx.cursor()
    questions = []

    question_ids = queryQuestions(cursor, select_tags)

    for id in question_ids:
            questions.append(id[0])

    if num_questions > len(questions):
        test = questions
    else:
        test = random.sample(questions, k=num_questions)

    # Insert test
    insert_test = ("INSERT INTO test(users_ID, is_tutor_mode, create_date, is_time_mode, test_name) VALUES(%s, %s, %s, %s, %s)")
    insert_test_values = []
    insert_test_values.append(users_id)
    insert_test_values.append(is_tutor_mode)    
    insert_test_values.append(date)
    insert_test_values.append(is_time_mode)
    insert_test_values.append(name)

    cursor.execute(insert_test, insert_test_values)
    cnx.commit()

    # Get inserted test id
    recent_test_query = ("""SELECT test_ID
                        FROM test
                        ORDER BY test_ID desc
                        LIMIT 1""")

    cursor.execute(recent_test_query)

    test_id = cursor.fetchall()[0][0]

    # Bridge test and questions
    for question in test:
        insert_test_question = ("INSERT INTO test_question(test_id, question_id) VALUES(%s, %s)")
        insert_test_question_values = []
        insert_test_question_values.append(test_id)
        insert_test_question_values.append(question)
        cursor.execute(insert_test_question, insert_test_question_values)
        cnx.commit()

    return test_id