import json
from flask import Flask, render_template, request, redirect, url_for, session,  flash, jsonify
import re
import mysql.connector
import os
import Answer, Question
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'verySecretKey'

UPLOAD_FOLDER = 'static/question_images'

# Checks if a file extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpeg', 'jpg'} 

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        question_text = request.form['questionInput']     
        example_text = request.form['explanationInput']   

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

        # Check if upload folder exists if not, create folder
        if os.path.isdir(UPLOAD_FOLDER) == False:
            os.mkdir(UPLOAD_FOLDER)

        # Checking to see if an image was given for the question
        if "image" not in request.files:
            flash('No Image')
        else:
            flash('Yes Image')
            image = request.files["image"]

            if image.filename != '' and allowed_file(image.filename):
                image.filename = 'question_' + str(question_id) + '.jpeg'
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('Invalid file. Please only choose a jpeg.')

        # Checking to see if an explanation image was given
        if "explanationImage" not in request.files:
            flash('No Image')
        else:
            flash('Yes Image')
            explanationImage = request.files["explanationImage"]

            if explanationImage.filename != '' and allowed_file(explanationImage.filename):
                print('name before')
                print(explanationImage.filename)
                explanationImage.filename = 'question_' + str(question_id) + '_explanation.jpeg'
                filename = secure_filename(explanationImage.filename)
                print('name after')
                print(filename)
                explanationImage.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('Invalid file. Please only choose a jpeg.')

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

        answer_texts = [] # THIS IS FOR SPRINT MEETING TO SHOWCASE
        for i in range(1, 7):
            insert_answer = "INSERT INTO answer(answer_text) VALUES (%s)"
            answer_text = request.form.get(f'answer{i}')

            if not answer_text == "":

                is_correct = 1 if request.form.get(f'correctAnswer{i}') else 0
                values = (answer_text,)
                cursor.execute(insert_answer, values)
                cnx.commit()
                answer_texts.append(answer_text)

                # Get answer id for answer1 
                query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer_text}\"")
                cursor.execute(query_answer)
                answer_id = cursor.fetchall()[0][0]

                # Insert answer id into question_answer bridging table
                insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
                values = (question_id, answer_id, is_correct)
                cursor.execute(insert_question_answer, values)
                cnx.commit()
            else:
                print(f"Answer {i} is None.")


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
        from make_attempt import makeAttempt
        date = str(date.today())

        test_id = makeTest(cnx, select_tags, number_of_questions, users_id, name_of_exam, isTutor, isTimed, date)
        attempt_num, attempt_id = makeAttempt(cnx, test_id)
        session['test_id'] = test_id
        session['attempt_num'] = attempt_num
        session['attempt_id'] = attempt_id


        return redirect(url_for('take_test', test_id=test_id, isTimed=isTimed, isTutor=isTutor))
    return render_template('createTest.html', firstName=firstName)

#   User is going to take test
@app.route('/testTemp', methods = ['GET', 'POST'])
@app.route('/testTemp.html', methods = ['GET', 'POST']) 
def take_test():

    test_id = request.args.get('test_id')
    isTimed = request.args.get('isTimed')
    isTutor = request.args.get('isTutor')


    # TODO CHECK IF TEST_ID IS LINKED WITH USER_ID IF NOT THROW 404

    cnx = dc.makeConnection()

    from get_test import getTest
    testSet = getTest(cnx, test_id)


    return render_template('testTemp.html', test_id=test_id, testList=testSet, isTimed=isTimed, isTutor=isTutor)

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
    userID = session.get('users_id')

    return render_template('viewTests.html')


import datetime 


@app.route('/submit_data', methods=['POST'])
def submit_data():

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

    from insert_answer import insertAnswer
    for state in question_states:
        # print(state)
        selected_answer = state.get('selectedAnswer') #Good
        question_id = state.get('questionID') #Good
        isCorrect = state.get('feedback')#Good, int val
        test_id = session.get('test_id')#Good, int val
        attempt_number = session.get('attempt_num') #Good, int val

        #Insert answer into database
        cnx = dc.makeConnection()
        insertAnswer(cnx, test_id, attempt_number, question_id, selected_answer, isCorrect)

    #Update attempt when exam is complete
    attempt_id = session.get('attempt_id')
    score = session.get('score')
    is_complete = 1
    time_taken = session.get('exam_time')   

    from update_attempt import updateAttempt
    cnx = dc.makeConnection()   
    updateAttempt(cnx, attempt_id, score, is_complete, time_taken)

    return jsonify({'message': 'Data received successfully'})

@app.route('/testResult')
@app.route('/testResult.html')
def testResult():

    

    examTime = session.get('exam_time')
    score = session.get('score')
    question_states = session.get('question_states')

    #Format for better output on results page. 
    format_time = datetime.timedelta(seconds=examTime)
    print("format_time: ", format_time)
    return render_template('testResult.html', examTime=format_time, score=score, question_states=question_states)

# Give a tag and the function will return all the questions that have that tag
@app.route('/searchQuestion', methods=['GET', 'POST'])
@app.route('/searchQuestion.html',methods=['GET', 'POST'])
def searchQuestion():

    # Gets the tag from the dropdown on the page
    tag = request.form.get('tagDropdown')
    
    #Calls the search_questions function using the tag, and putting it in a variable
    tagQuestions = search_question(tag)
 
    #Passes the question list to searchQuestions.html 
    return render_template('searchQuestion.html', tagQuestions = tagQuestions)


# Give a tag and the function will return all the questions that have that tag
def search_question(tag):

    
    # Start connection
    cnx = dc.makeConnection()
    cursor = cnx.cursor()
    
    
    # tag to search questions from
    question_tag = tag

    # querying from the database for questions that have tag
    query = (f"""SELECT q.question_ID, q.question_text, t.tag_name AS 'tag' 
             FROM omm.question q
            JOIN omm.tag_question tq ON (q.question_ID = tq.question_ID)
            JOIN omm.tag t ON (tq.tag_ID = t.tag_ID)
            WHERE q.is_active = 1 AND t.tag_name = \"{question_tag}\"; """)
    cursor.execute(query)

    results = cursor.fetchall()

    #current question
    index = 0

    questions = []

    # Storing all the questions into dictionaries and then into the questions list
    for question in results:
        searchResult = {
            'questionID' : results[index][0],
            'questionText' : results[index][1],
            'tag' : results[index][2]
        }

        questions.append(searchResult)

        index += 1

    # Printing out new list of dictionaries
    # for question in questions:
    #     print("new dictionaries")
    #     print("Question ID:")
    #     print(question['questionID'])
    #     print("Question Text:")
    #     print(question['questionText'])
    #     print("Tag:")
    #     print(question['tag'])


     #Close connection
    cnx.close()
    cursor.close()

    return questions

# Give a question_ID and it will return that question in a Question object
def store_question(ID):

    # Start connection
    cnx = dc.makeConnection()
    cursor = cnx.cursor()
    
    # Give a question ID
    question_ID = ID

    # Get question
    query = (f"""select q.question_ID, question_text, example_text, GROUP_CONCAT(CONCAT( "[", a.answer_ID, ":", answer_text, ":", is_correct, "]")) as answers
                from omm.question q
                join omm.question_answer qa on qa.question_ID = q.question_ID
                join omm.answer a on a.answer_ID = qa.answer_ID
                where q.question_ID = {question_ID} and q.is_active = 1
                group by q.question_ID, q.question_text, q.example_text;""")

    cursor.execute(query)

    # Get results from query
    return_value = cursor.fetchall()

    # Get the answers
    answer_objects = []
    answers  = return_value[0][3].replace("],[", "]|[").split("|")

    for answer in answers:
        id = answer[1:-1].split(":")[0]
        text = answer[1:-1].split(":")[1]
        is_correct = answer[1:-1].split(":")[2]

        answer = Answer.Answer(id, text, is_correct)
        answer_objects.append(answer)

    # Create question object
    question = Question.Question(return_value[0][0], return_value[0][1], return_value[0][2], answer_objects)

    # Print out results
    # print("Question ID:")
    # print(question.getID())
    # print("Question Text:")
    # print(question.getQuestionText())
    # print("Example Text:")
    # print(question.getExampleText())
    # print("Answers:")

    # for answer in question.getAnswers():
    #     print(answer.getAnswerText())
    #     print(answer.getIsCorrect())
    #     print(answer.getAnswerID())

    question_id = question.getID()

    # creating the names for what images to get for a specific question id
    filenameImage = 'question_' + str(question_id) + '.jpeg'
    filenameExplanationImage = 'question_' + str(question_id) + '_explanation.jpeg'
    pathToImage = UPLOAD_FOLDER + "/" + filenameImage
    pathToExplanationImage = UPLOAD_FOLDER + "/" + filenameExplanationImage

    # store image to question
    if os.path.isfile(pathToImage):
        print("Success Success Success")
        question.setImage(filenameImage)
        print(filenameImage)
    else:
        print("Fail Fail Fail")
        print(question_id)

    # store explanation image to question
    if os.path.isfile(pathToExplanationImage):
        print("Success Success Success")
        question.setExplanationImage(filenameExplanationImage)  
        print(filenameExplanationImage)
    else:
        print("Fail Fail Fail")
        print(question_id)

    #Close connection
    cnx.close()
    cursor.close()

    return question

# Give a tag and the function will return all the questions that have that tag
def search_question(tag):
    # Start connection
    cnx = dc.makeConnection()
    cursor = cnx.cursor()
    
    # tag to search questions from
    question_tag = tag

    # querying from the database for questions that have tag
    query = (f"""SELECT q.question_ID, q.question_text, t.tag_name AS 'tag' 
             FROM omm.question q
            JOIN omm.tag_question tq ON (q.question_ID = tq.question_ID)
            JOIN omm.tag t ON (tq.tag_ID = t.tag_ID)
            WHERE q.is_active = 1 AND t.tag_name = \"{question_tag}\"; """)
    cursor.execute(query)

    results = cursor.fetchall()

    #current question
    index = 0

    questions = []

    # Storing all the questions into dictionaries and then into the questions list
    for question in results:
        searchResult = {
            'questionID' : results[index][0],
            'questionText' : results[index][1],
            'tag' : results[index][2]
        }

        questions.append(searchResult)

        index += 1

    # Printing out new list of dictionaries
    # for question in questions:
    #     print("new dictionaries")
    #     print("Question ID:")
    #     print(question['questionID'])
    #     print("Question Text:")
    #     print(question['questionText'])
    #     print("Tag:")
    #     print(question['tag'])


     #Close connection
    cnx.close()
    cursor.close()

    return questions

# Given the old Question object, insert a new question 
def edit_question(oldQuestion): 

    # Get question_text and example_text
    question_text = request.form['questionInput']     
    example_text = request.form['explanationInput']   

    # Get users id (faculty who created the question)
    user_id = session.get('users_id')

    # Start connection
    cnx = dc.makeConnection()
    cursor = cnx.cursor()

    # Disable old question 
    remove_old_question = (f"""UPDATE question
                           SET is_active = 0
                           WHERE question_ID = {oldQuestion.getID()}""")
    cursor.execute(remove_old_question)
    cnx.commit()

    # Insert question text, example text, is_active (Default 1), users_id (Work in Progress)
    insert_question = ("INSERT INTO question(question_text, example_text, is_active, users_ID) VALUES(%s, %s, %s, %s)")
    values = (question_text, example_text, 1, user_id)
    cursor.execute(insert_question, values)
    cnx.commit()

    # Get question id for question we just added
    query_question = (f"SELECT question_ID FROM question WHERE question_text = \"{question_text}\" AND is_active = 1")
    cursor.execute(query_question)
    question_id = cursor.fetchall()[0][0]

     # Checking to see if an image was given for the question
    if "image" not in request.files:
        flash('No Image')
    else:
        flash('Yes Image')
        image = request.files["image"]

        if image.filename != '' and allowed_file(image.filename):
            image.filename = 'question_' + str(question_id) + '.jpeg'
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            flash('Invalid file. Please only choose a jpeg.')

    # Checking to see if an explanation image was given
    if "explanationImage" not in request.files:
        flash('No Image')
    else:
        flash('Yes Image')
        explanationImage = request.files["explanationImage"]

        if explanationImage.filename != '' and allowed_file(explanationImage.filename):
            explanationImage.filename = 'question_' + str(question_id) + '_explanation.jpeg'
            filename = secure_filename(explanationImage.filename)
            explanationImage.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            flash('Invalid file. Please only choose a jpeg.')

    

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

    # Old answers from previous question
    answers = oldQuestion.getAnswers()

    answer_texts = [] # THIS IS FOR SPRINT MEETING TO SHOWCASE
    for i in range(1, 6):
        insert_answer = "INSERT INTO answer(answer_text) VALUES (%s)"
        answer_text = request.form.get(f'answer{i}')

        if answer_text is not None:

            is_correct = 1 if request.form.get(f'correctAnswer{i}') else 0
            
            # Check to make sure that the answer is not already in the database
            if answers[i-1].getAnswerText() != answer_text:
                
                values = (answer_text,)
                cursor.execute(insert_answer, values)
                cnx.commit()
                answer_texts.append(answer_text)

            # Get answer id for answer1 
            query_answer = (f"SELECT answer_ID FROM answer WHERE answer_text = \"{answer_text}\"")
            cursor.execute(query_answer)
            answer_id = cursor.fetchall()[0][0]

            # Insert answer id into question_answer bridging table
            insert_question_answer = ("INSERT INTO question_answer(question_ID, answer_ID, is_correct) VALUES(%s, %s, %s)")
            values = (question_id, answer_id, is_correct)
            cursor.execute(insert_question_answer, values)
            cnx.commit()
        else:
            print(f"Answer {i} is None.")

    #Close connection
    cnx.close()
    cursor.close()

# Give a question ID and this function will disable it in the database
def delete_question(ID):

    question_ID = ID

   # Start connection
    cnx = dc.makeConnection()
    cursor = cnx.cursor()

    # Disable old question 
    remove_question = (f"""UPDATE question
                       SET is_active = 0
                       WHERE question_ID = {question_ID}""")
    cursor.execute(remove_question)
    cnx.commit()

    #Close connection
    cnx.close()
    cursor.close()

if __name__ == '__main__':
    app.run(debug=True, port=8000) 
