from flask import redirect, render_template, request, session, url_for
from database_connection import makeConnection


def create():
    firstName = session.get('user_firstName') 
    if request.method == 'POST':
        #Start connection
        cnx = makeConnection()
        
        isTutor = False
        isTimed = False
        if request.form.get("tutoredTest"):
            isTutor = True
        
        if request.form.get("timedTest"):
            isTimed = True
        # TODO MAKE SURE TO CHANGE FORM VALUES FOR SELECTED_TAGS
        # TODO TELL FRONTEND TO ADD IN MISSING TAGS
        
        select_tags = request.form.getlist('category') # contains list of categories chosen
        number_of_questions = int(request.form.get('numberInput')) # holds the number of questions student entered
        users_id = session.get('users_id') # Grab current person logged in user_id

        name_of_exam = "test"    #TODO Add in form to allow student to name exam?    

        from DatabaseFunctions.make_test import makeTest
        from datetime import date
        from DatabaseFunctions.make_attempt import makeAttempt
        date = str(date.today())

        test_id = makeTest(cnx, select_tags, number_of_questions, users_id, name_of_exam, isTutor, isTimed, date)
        attempt_num, attempt_id = makeAttempt(cnx, test_id)
        session['test_id'] = test_id
        session['attempt_num'] = attempt_num
        session['attempt_id'] = attempt_id


        return redirect(url_for('take_test', test_id=test_id, isTimed=isTimed, isTutor=isTutor))
    return render_template('createTest.html', firstName=firstName)