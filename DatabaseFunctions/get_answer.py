def getAnswer(cnx, test_id, attempt_num, question_id):

    cursor = cnx.cursor()

    query = (f"""select answer_id
            from attempt a
            join attempt_answer an on an.attempt_id = a.attempt_id
            where test_id = {test_id} and attempt_number = {attempt_num} and question_id = {question_id};""")

    cursor.execute(query)

    result = cursor.fetchall()

    return result[0][0]