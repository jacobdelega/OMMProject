from flask import Flask, render_template, request, redirect, url_for, session,  flash
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'verySecretKey'

#   Setting up the connection to local SQL database
def connectDataBase():
    return mysql.connector.connect(
        host = '127.0.0.1',
        user='root',
        password='NULL',
        database='OMMProject'
    )

#   Test Successful Connection
@app.route('/test_database')
@app.route('/test_database.html')
def testDataBase():

    #   Initialize connection
    dbConnect = connectDataBase()
    cursor = dbConnect.cursor()

    #   Grab data
    query = "SELECT * from userAccounts LIMIT 1000"
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
        username = request.form['email']
        password = request.form['password']
        #   Start connection
        dbConnect = connectDataBase()
        cursor = dbConnect.cursor()

        #   Select username and password that match given
        query = 'SELECT * FROM userAccounts WHERE email = %s AND password = %s'
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        #   Close Connection
        
        if user:
            user_id = user[0]
            username = user[1]
            email = user[2]
            session['user_id'] = user_id
            session['username'] = username
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid login", 'Invalid credentials')
    return render_template('index.html')

#   user auth complete, send to dashboard
@app.route('/dashboard')
@app.route('/dashboard.html')
def dashboard():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']

    #     if email in session:
    #         email = session.get('email')
    username = session.get('username')
    if username:
        return render_template('dashboard.html', username=username)
    else:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('index'))
    



if __name__ == '__main__':
    app.run(debug=True, port=3030)