from flask import Flask, render_template, request, redirect, url_for, session,  flash
import re
import mysql.connector

app = Flask(__name__)
app.secret_key = 'verySecretKey'

#   Setting up the connection to local SQL database
def connectDataBase():
    return mysql.connector.connect(
        host = '3.87.120.222',
        user='delega25',
        password='OMMProject',
        database='omm'
    )

#   Test Successful Connection
@app.route('/test_database')
@app.route('/test_database.html')
def testDataBase():

    #   Initialize connection
    dbConnect = connectDataBase()
    cursor = dbConnect.cursor()

    #   Grab data
    query = "SELECT q.example_text, q.is_active, qa.is_correct, a.answer_text, t.dtype, t.tag_name FROM question q  LEFT JOIN question_answer qa  ON  qa.question_ID = q.question_ID LEFT JOIN answer a ON a.answer_ID = qa.answer_ID LEFT JOIN tag_question tq ON tq.question_ID = q.question_ID LEFT JOIN tag t ON t.tag_ID = tq.tag_ID"
    cursor.execute(query)
    results = cursor.fetchall()

    #   close connection
    cursor.close()
    dbConnect.close()

    return render_template('test_database.html', results=results)

#   Get user to login
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index.html', methods = ['GET', 'POST'])
def login():

    #   Grab user info
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #   Start connection
        dbConnect = connectDataBase()
        cursor = dbConnect.cursor()

        #   Select username and password that match given
        query = 'SELECT * FROM users WHERE email = %s AND pass = %s'
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        #   Close Connection

        if user:
            users_id = user[0] 
            user_firstName = user[2]
            user_email = user[4]
            session['users_id'] = users_id
            session['user_firstName'] = user_firstName
            session['user_email'] = user_email
            print("Session data:", session)
            return redirect(url_for('home'))
        else:
            flash("Invalid login", 'Invalid credentials')

        #Close connection
        dbConnect.close()
        cursor.close()
    return render_template('index.html')


#   user auth complete, send them to home page
@app.route('/home')
@app.route('/home.html')
def home():
    firstName = session.get('user_firstName')
    if firstName:
        return render_template('home.html', firstName = firstName)
    else:
        flash("please log in to access the dashboard.", 'error')
        return redirect(url_for('index.html'))
    return render_template('home.html')


@app.route('/dashboard')
@app.route('/dashboard.html')
def dashboard():

    user_email = session.get('user_email')
    if user_email:
        return render_template('home.html', user_email=user_email)
    else:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('index'))

import database_connection as dc
#   User wants to go to create test page
@app.route('/createTest', methods=['POST', 'GET'])
@app.route('/createTest.html', methods=['POST', 'GET'])
def createTest():
    firstName = session.get('user_firstName') 
    if request.method == 'POST':
        
        #Start connection
        cnx = dc.makeConnection()
        
        isTutor = False
        isTimed = False
        if request.form.get("tutoredTest"):
            isTutor = True
        
        if request.form.get("timedTest"):
            isTimed = True
        # TODO MAKE SURE TO CHANGE FORM VALUES FOR SELECTED_TAGS
        # TODO TELL FRONTEND TO ADD IN MISSING TAGS

        select_tags = request.form.getlist('tag_question') # contains list of tags
        number_of_questions = int(request.form.get('numberInput')) # holds the number of questions student entered
        users_id = session.get('users_id') # Grab current person logged in user_id

        name_of_exam = "testv2"    #TODO Add in form to allow student to name exam?    

        from make_test import makeTest
        from datetime import date
        date = str(date.today())

        test_id = makeTest(cnx, select_tags, number_of_questions, users_id, name_of_exam, isTutor, isTimed, date)
        return redirect(url_for('take_test', test_id=test_id))
    return render_template('createTest.html', firstName=firstName)

#   User is going to take test
@app.route('/test', methods = ['GET', 'POST'])
@app.route('/test.html', methods = ['GET', 'POST']) 
def take_test():

    # checking if the answer is correct
    msg = ""
    if request.method == 'POST':
        answerID = request.form['answerID']
        if testSet.getCurrentQuestion().checkAnswer('answerID'):
            msg = "Correct!"
        elif testSet.getCurrentQuestion().checkAnswer('answerID') == False:
            msg = "Sorry, incorrect."

    test_id = request.args.get('test_id')
    cnx = dc.makeConnection()

    from get_test import getTest
    testSet = getTest(cnx, test_id)
    # print(testSet.getPrevQuestion().getQuestionText())

    return render_template('test.html', test_id=test_id, testList=testSet)

#   User wants to go to view statistics
@app.route('/viewStats')
@app.route('/viewStats.html')
def viewStats():
    return render_template('viewStats.html')

#   User wants to go to view tests
@app.route('/viewTests')
@app.route('/viewTests.html')
def viewTests():
    return render_template('viewTests.html')

#   Adding a question
@app.route('/addQuestion')
@app.route('/addQuestion.html')
def addQuestion():
    question_text = "What is a human?"      # Temp value
    example_text = "A human is a living being that walk on two legs."  #Temp value

    # Get users id (faculty who created the question)
    user_id = session.get('users_id')

    # Start connection
    cnx = dc.makeConnection()
    cursor = cnx.cursor()

    # Insert question text, example text, is_active (Default 1), users_id (Work in Progress)
    insert_question = ("INSERT INTO question(question_text, example_text, is_active, users_ID) VALUES(%s, %s, %s, %s)")
    values = (question_text, example_text, 1, user_id)
    cursor.execute(insert_question, values)
    cnx.commit()

    # Get question id for question we just added
    query_question = (f"SELECT question_ID FROM question WHERE question_text = \"{question_text}\"")
    cursor.execute(query_question)
    question_id = cursor.fetchall()[0][0]





    # For tags, loop through all the tags and see which one are checked
    # Then query for the tag id and insert into tag_question before moving on to
    # The next tag
    """
    for tag in taglist:
        query_question = (f"SELECT tag_ID FROM question WHERE question_text = \"{question_text}\"")
        cursor.execute(query_question)
        question_id = cursor.fetchall()[0][0]
    """





    # Assume answers will be in their own textbox and each one will have 
    # another radio button showing which one is correct
    # check to see if the fifth answer is null (none)
    answer1 = "Answer 1 for this question"
    answer2 = "Answer 2 for this question"
    answer3 = "Answer 3 for this question"
    answer4 = "Answer 4 for this question"
    is_Correct1 = 0
    is_Correct2 = 0
    is_Correct3 = 0
    is_Correct4 = 1

    # Insert answer1 into answer table
    insert_answer = (f"INSERT INTO answer(answer_text) VALUES(%s)")
    values = (answer1)
    cursor.execute(insert_answer, values)
    cnx.commit()

    # Get answer id for answer1 
    query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer1}\"")
    cursor.execute(query_answer)
    answer_id = cursor.fetchall()[0][0]

    # Insert answer1 into question_answer bridging table
    insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
    values = (question_id, answer_id, is_Correct1)
    cursor.execute(insert_question_answer, values)
    cnx.commit()



    # Insert answer2 into answer table
    values = (answer2)
    cursor.execute(insert_answer, values)
    cnx.commit()

    # Get answer id for answer2
    query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer2}\"")
    cursor.execute(query_answer)
    answer_id = cursor.fetchall()[0][0]

    # Insert answer2 into question_answer bridging table
    insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
    values = (question_id, answer_id, is_Correct2)
    cursor.execute(insert_question_answer, values)
    cnx.commit()



    # Insert answer3 into answer table
    values = (answer3)
    cursor.execute(insert_answer, values)
    cnx.commit()

    # Get answer id for answer3
    query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer3}\"")
    cursor.execute(query_answer)
    answer_id = cursor.fetchall()[0][0]

    # Insert answer3 into question_answer bridging table
    insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
    values = (question_id, answer_id, is_Correct3)
    cursor.execute(insert_question_answer, values)
    cnx.commit()



    # Insert answer4 into answer table
    values = (answer4)
    cursor.execute(insert_answer, values)
    cnx.commit()

    # Get answer id for answer4
    query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer4}\"")
    cursor.execute(query_answer)
    answer_id = cursor.fetchall()[0][0]

    # Insert answer4 into question_answer bridging table
    insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
    values = (question_id, answer_id, is_Correct4)
    cursor.execute(insert_question_answer, values)
    cnx.commit()



    # Do insert answer 5
    """
    if (answer5HTML != ''):
        answer5 = answer5HTML
        is_Correct5 = 0

        # Insert answer5 into answer table
        values = [(answer5)]
        cursor.execute(insert_answer, values)
        cnx.commit()

        # Get answer id for answer5
        query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer5}\"")
        cursor.execute(query_answer)
        answer_id = cursor.fetchall()[0][0]

        # Insert answer5 into question_answer bridging table
        insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
        values = (question_id, answer_id, is_Correct5)
        cursor.execute(insert_question_answer, values)
        cnx.commit()
    
    """

    

    


if __name__ == '__main__':
    app.run(debug=True) 
