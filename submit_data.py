from flask import request, session, jsonify
from database_connection import makeConnection


def submit():
    data = request.json
    question_states = data.get('questionStates', [])
    session['question_states'] = question_states

    last_question = question_states[-1] # Only needed to grab the score and the time

    if 'time' in last_question:
        submitted_time = last_question['time']
        print("Submitted Time:", submitted_time)

        session['exam_time'] = submitted_time
    else:
        session['exam_time'] = 0
    
    if 'score' in last_question:
        session['score'] = last_question['score']

    from DatabaseFunctions.insert_answer import insertAnswer
    for state in question_states:
        # print(state)
        selected_answer = state.get('selectedAnswer') #Good
        question_id = state.get('questionID') #Good
        isCorrect = state.get('feedback')#Good, int val
        test_id = session.get('test_id')#Good, int val
        attempt_number = session.get('attempt_num') #Good, int val

        #Insert answer into database
        cnx = makeConnection()
        insertAnswer(cnx, test_id, attempt_number, question_id, selected_answer, isCorrect)

    #Update attempt when exam is complete
    attempt_id = session.get('attempt_id')
    score = session.get('score')
    is_complete = 1
    time_taken = session.get('exam_time')   

    from DatabaseFunctions.update_attempt import updateAttempt
    cnx = makeConnection()   
    updateAttempt(cnx, attempt_id, score, is_complete, time_taken)

    return jsonify({'message': 'Data received successfully'})