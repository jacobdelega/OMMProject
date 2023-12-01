from flask import Flask, render_template, request, redirect, url_for, session,  flash, jsonify
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
            user_state = user[1] 
            user_firstName = user[2]
            user_email = user[4]
            session['users_id'] = users_id
            session['user_state'] = user_state
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

#   Adding a question
@app.route('/addQuestion', methods=['GET', 'POST'])
@app.route('/addQuestion.html', methods=['GET', 'POST'])
def addQuestion():

    if request.method == 'POST':


        question_text = request.form['questionInput'] #"What is a human?"      # Temp value
        example_text = request.form['explanationInput'] #"A human is a living being that walk on two legs."  #Temp value

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

        selected_tags = request.form.getlist('subjectDropdown')

        # For tags, loop through all the tags and see which one are checked
        # Then query for the tag id and insert into tag_question before moving on to
        # The next tag
        for tag in selected_tags:
            query_tag = (f"SELECT tag_ID FROM tag WHERE tag_name = \"{tag}\"")
            cursor.execute(query_tag)
            tag_id = cursor.fetchall()[0][0]

            insert_tag_question = (f"INSERT INTO tag_question(tag_ID, question_ID) VALUES(%s, %s)")
            values = (tag_id, question_id)
            cursor.execute(insert_tag_question, values)
            cnx.commit()

        # insert_answer = (f"INSERT INTO answer(answer_text) VALUES(%s)")
        answer_texts = [] # THIS IS FOR SPRINT MEETING TO SHOWCASE
        for i in range(1, 6):
            insert_answer = "INSERT INTO answer(answer_text) VALUES (%s)"
            answer_text = request.form.get(f'answer{i}')
            
            if answer_text is not None:
                is_correct = 1 if request.form.get(f'correctAnswer{i}') else 0
                values = (answer_text,)
                cursor.execute(insert_answer, values)
                cnx.commit()
                answer_texts.append(answer_text)
            else:
                print(f"Answer {i} is None.")

            # Get answer id for the current answer 
            query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer_text}\"")
            cursor.execute(query_answer)
            answer_id = cursor.fetchall()[0][0]

            # Insert answer id into question_answer bridging table
            insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
            values = (question_id, answer_id, is_correct)
            cursor.execute(insert_question_answer, values)
            cnx.commit()


        return redirect(url_for('success_page', question_text = question_text, question_id = question_id, answer_id = answer_id, is_correct=is_correct, answer_texts=answer_texts))
    return render_template('addQuestion.html')

#   user auth complete, send them to home page
@app.route('/home')
@app.route('/home.html')
def home():
    firstName = session.get('user_firstName')
    user_state = session.get('user_state')
    if firstName:
        return render_template('home.html', firstName = firstName, user_state = user_state)
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

        select_tags = request.form.getlist('category') # contains list of categories chosen
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
@app.route('/testTemp', methods = ['GET', 'POST'])
@app.route('/testTemp.html', methods = ['GET', 'POST']) 
def take_test():

    test_id = request.args.get('test_id')
    
    # TODO CHECK IF TEST_ID IS LINKED WITH USER_ID IF NOT THROW 404

    cnx = dc.makeConnection()

    from get_test import getTest
    testSet = getTest(cnx, test_id)

    return render_template('testTemp.html', test_id=test_id, testList=testSet)

#   User wants to go to view statistics
@app.route('/viewStats')
@app.route('/viewStats.html')
def viewStats():
    return render_template('viewStats.html')

@app.route('/success_page')
@app.route('/success_page.html')
def success_page():
    question_id = request.args.get('question_id')
    answer_id = request.args.get('answer_id')
    is_correct = request.args.get('is_correct')
    answer_texts = request.args.getlist('answer_texts')
    question_text = request.args.get('question_text')
    
    return render_template('success_page.html', question_text = question_text, answer_texts=answer_texts, question_id = question_id, answer_id = answer_id, is_correct=is_correct)

#   User wants to go to view tests
@app.route('/viewTests')
@app.route('/viewTests.html')
def viewTests():
    return render_template('viewTests.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    question_states = data.get('questionStates', [])


    print(question_states)
    # Process the received data as needed
    # ...

    return jsonify({'message': 'Data received successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=8000) 