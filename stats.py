def getStats(cnx, student_id):
    cursor = cnx.cursor()

    # get total number of questions for each tag type
    query = ("""select * from vw_question_tags_count""")

    cursor.execute(query)

    columns = cursor.description 
    result = cursor.fetchall()

    question_tags_count = {}

    for i,column in enumerate(columns):
        question_tags_count.update({column[0] : str(result[0][i])})

    # get total attempted question count for each tage type
    query = (f"""select * from vw_attempted_question_tags_count where users_id = {student_id}""")

    cursor.execute(query)

    columns = cursor.description 
    result = cursor.fetchall()

    attempted_question_tags_count = {}

    for i,column in enumerate(columns):
        attempted_question_tags_count.update({column[0] : str(result[0][i])})

    # get total attempted question correct count for each tage type
    query = (f"""select * from vw_attempted_question_tags_correct_count where users_id = {student_id}""")

    cursor.execute(query)

    columns = cursor.description 
    result = cursor.fetchall()

    attempted_question_tags_correct_count = {}

    for i,column in enumerate(columns):
        attempted_question_tags_correct_count.update({column[0] : str(result[0][i])})

    # calculate percents and put everything into a dict
    result = {}

    for tag in question_tags_count.keys():

        total = int(question_tags_count.get(tag))
        attempted = int(attempted_question_tags_count.get(tag))
        unattempted = total - attempted
        right = int(attempted_question_tags_correct_count.get(tag))
        wrong = attempted - right

        unattempted_p = (unattempted / total) * 100
        right_p = (right / total) * 100
        wrong_p = (wrong / total) * 100

        result.update({tag: {'unattempted' : unattempted_p, 'wrong' : right_p, 'right' : wrong_p}})

    print(result)
    cnx.close()

    return result