from hashlib import sha256
from flask import Flask, render_template, request, redirect, url_for, session,  flash
from database_connection import makeConnection

def signUpUser():

    msg = ""

    if request.method == 'POST':
        dbConnect = makeConnection()
        cursor = dbConnect.cursor()

        firstName = request.form['fName']
        lastName = request.form['lName']
        password = request.form['password']
        email = request.form['email']

        elligibleToCreateUser = True


        cursor.execute('SELECT * FROM users WHERE email = %s', (email, ))
        account = cursor.fetchone()

        cursor.close()


        if account: #If that account already exists, we won't let the user create that account.
            msg = "Account already exists with that email\n"
            elligibleToCreateUser = False
        
        #Checks to make sure
        if not email:
            msg += "Email required\n"
            elligibleToCreateUser = False

        if not firstName:
            msg += "First name required\n"
            elligibleToCreateUser = False

        if not lastName:
            msg += "Last name required\n"
            elligibleToCreateUser = False

        if not password:
            msg += "Password required\n"
            elligibleToCreateUser = False

        #If the account doesn't already exists
        if elligibleToCreateUser:
            password = sha256(password.encode('utf-8')).hexdigest() #encrypts the password before we pass it in to the users' table.
            
            userCursor = dbConnect.cursor()
            idCursor = dbConnect.cursor()

            #Creating a student
            if request.form['button'] == "studentButton":
                userCursor.execute('INSERT INTO users(dtype, first_name, last_name, email, pass) VALUES ("student", %s, %s, %s, %s)', (firstName, lastName, email, password, ))
                dbConnect.commit()
                newUserID = getID(email)
                idCursor.execute('INSERT INTO student(users_ID) VALUES(%s)', (newUserID, ))


            #Creating a faculty member
            if request.form['button'] == "facultyButton":
                userCursor.execute('INSERT INTO users(dtype, first_name, last_name, email, pass) VALUES ("faculty", %s, %s, %s, %s)', (firstName, lastName, email, password, ))
                dbConnect.commit()
                newUserID = getID(email)
                idCursor.execute('INSERT INTO faculty(users_ID) VALUES(%s)', (newUserID, ))
                userCursor.execute('INSERT INTO student(users_ID) VALUES(%s)', (newUserID, ))

            userCursor.close()
            idCursor.close() #Closing all connections
            
            dbConnect.commit() #Committing all of the information to the database
            return redirect('/index')
        
    return render_template("signup.html", msg = msg)



def getID(email):
    dbConnect = makeConnection()
    cursor = dbConnect.cursor()

    cursor.execute("SELECT users_ID FROM users WHERE email=%s", (email, ))
    id = cursor.fetchone()[0] #[0] is the ID in the 2D list returned from the database
    
    cursor.close()
    dbConnect.close()

    return id 