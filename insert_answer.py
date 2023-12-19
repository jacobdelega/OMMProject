# This function updates a single answer for an attempt
def insertAnswer(cnx, test_id, attempt_number, question_id, answer_id, is_correct):

    cursor = cnx.cursor()
    
    query = (f"""select attempt_answer_ID, answer_ID
            from attempt a
            join attempt_answer an on an.attempt_ID = a.attempt_ID
            where test_ID = {test_id} and attempt_number = {attempt_number} and question_id = {question_id}""")

    cursor.execute(query)

    results = cursor.fetchall()
    attempt_answer_id = results[0][0]

    if results[0][1] == None:
        # insert answer to question
        # convert is_correct to int
        is_correct = int(is_correct)
        answer_id = int(answer_id)
        update_answer = (f"""update attempt_answer
                        SET answer_ID = {answer_id},
                            is_correct = {is_correct}
                        where attempt_answer_ID = {attempt_answer_id}""")
        
        cursor.execute(update_answer)
        cnx.commit()
    else:
        print('Question already answered.')

    cnx.close()