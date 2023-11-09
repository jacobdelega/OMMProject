from flask import Flask, render_template, request, redirect, url_for, session,  flash
import re
import mysql.connector
import testSet, Question
import get_test
# from t import getTestSet

app = Flask(__name__)
app.secret_key = 'verySecretKey'

# var1 = testSet.testSet()
# var1.addQuestion(Question.Question(1, "A 62-year-old male presents to the office for right elbow pain for three days. He reports that he tripped and fell backwards but was able to break his fall with his outstretched right hand. He denies any trauma to the head or other parts of his body. Structural examination reveals an increased carrying angle of the right arm. Which of the following findings is likely to be found on physical examination of the right arm?", "The question describes an anterior radial head dysfunction (supination dysfunction) with an increased carrying angle. If the carrying angle were increased, the ulna would deviate more laterally, the radius would move inferiorly, and the carpal bones would move medially. Thus, expected physical findings would be increased forearm abduction, increased inferior glideof the radius, and increased adduction of the wrist. ", "[Increased forearm abduction, increased inferior glide of the radius and increased adduction of the wrist :1 ], [Increased forearm adduction, increased inferior glide of the radius and increased adduction of the wrist: 0], [Increased forearm abduction,increased superior glide of the radius and increased adduction of the wrist: 0], [Increased forearm adduction, increased superior glide of the radius and increased abduction of the wrist: 0], [Increased forearm abduction, increased superior glide of the radius and increased abduction of the wrist: 0] " ))

# var1 = getTestSet() #returns full test set

var1 = get_test.getTest(1)

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

@app.route('/test')
@app.route('/test.html')
def takeTest():
    return render_template('testTemp.html', testList = var1)
    

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

#   User wants to go to create test page
@app.route('/createTest', methods=['POST', 'GET'])
@app.route('/createTest.html', methods=['POST', 'GET'])
def createTest():
    firstName = session.get('user_firstName') 
    if request.method == 'POST':
        
        #Start connection
        cnx = connectDataBase.makeConnection()
        
        isTutor = False
        isTimed = False
        if request.form.get("tutoredTest"):
            isTutor = True
        
        if request.form.get("timedTest"):
            isTimed = True

        select_tags = request.form.getlist('tag_question') # contains list of tags
        number_of_questions = int(request.form.get('numberInput')) # holds the number of questions student entered
        users_id = session.get('users_id') # Grab current person logged in user_id

        name_of_exam = "test"    #TODO Add in form to allow student to name exam?    

        from make_test import makeTest
        from datetime import date
        date = str(date.today())

        test_id = makeTest(cnx, select_tags, number_of_questions, users_id, name_of_exam, isTutor, isTimed, date)

        return render_template('test_result.html', test_id=test_id)
    
        #Close connection
    return render_template('createTest.html', firstName=firstName)

#   User is going to take test
@app.route('/test_result', methods = ['GET', 'POST'])
@app.route('/test_result.html', methods = ['GET', 'POST']) 
def take_test():

    test_id = request.args.get('test_id')

    return render_template('test_result.html', test_id=test_id)

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


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='localhost') 
