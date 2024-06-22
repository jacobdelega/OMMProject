import database_connection as dc
from datetime import date
from database_connection import makeConnection

# This function takes a created test and makes a new attempt in the database
def makeAttempt(cnx, test_id):
    cursor = cnx.cursor()
    
    # cursor = makeConnection().cursor()

    # query to get users_id for student given a test
    student_id_query = (f"""select users_id
                        from test
                        where test_ID = {test_id};
                        """)
    
    cursor.execute(student_id_query)

    student_id = cursor.fetchall()[0][0]

    today = date.today()

    # set attempt number
    attempt_query = (f"""select attempt_number 
                     from attempt 
                     where test_id = {test_id}
                     ORDER BY attempt_number desc
                     LIMIT 1""")

    cursor.execute(attempt_query)

    result = cursor.fetchall()

    # print(result)

    if not result:
        attempt_num = 1
    else:
        attempt_num = result[0][0] + 1

    # insert attempt into attempt table
    insert_test = ("INSERT INTO attempt(test_ID, users_ID, attempt_date, is_complete, attempt_number) VALUES(%s, %s, %s, %s, %s)")
    insert_test_values = []
    insert_test_values.append(test_id)
    insert_test_values.append(student_id)    
    insert_test_values.append(today)
    insert_test_values.append(0)
    insert_test_values.append(attempt_num)

    cursor.execute(insert_test, insert_test_values)
    cnx.commit()
    # print('inserted attempt')

    # get id of created attempt
    recent_attempt_query = ("""SELECT attempt_ID
                        FROM attempt
                        ORDER BY attempt_ID desc
                        LIMIT 1""")
    
    cursor.execute(recent_attempt_query)

    attempt_id = cursor.fetchall()[0][0]

    # query to get question_ids for a test
    question_ids_query = (f"""select GROUP_CONCAT(question_id)
                          from test_question
                          where test_ID = {test_id}""")
    
    cursor.execute(question_ids_query)
    
    questions = str(cursor.fetchall()[0][0]).split(",")

    for question in questions:
        question_id = question

        insert_attempt_answer = ("insert into attempt_answer(attempt_ID, question_ID) VALUES(%s, %s)")
        insert_attempt_answer_values = []
        insert_attempt_answer_values.append(attempt_id)
        insert_attempt_answer_values.append(question_id)

        cursor.execute(insert_attempt_answer, insert_attempt_answer_values)
        cnx.commit()
        # print(f'Inserted question: {question_id}')

    return attempt_num, attempt_id