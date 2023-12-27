import os
from DatabaseFunctions import get_question
from flask import flash, redirect, render_template, request, session, url_for
from database_connection import makeConnection
from werkzeug.utils import secure_filename


def editQuestionByID(id, UPLOAD_FOLDER):
    question = get_question.getquestionfromdatabase(id)
    # question_text = question.getQuestionText()
    # question_id = question.getID()
    if request.method == 'POST':
        if request.form['button'] == "editQuestion":
            id = edit_question(question, UPLOAD_FOLDER)
            session['edited_question_id'] = id # Grab new id after edited 
            question = get_question.getquestionfromdatabase(id)
            return redirect(url_for('success_page', question= question))
    return render_template('editQuestion.html', question = question)



# Given the old Question object, insert a new question 
def edit_question(oldQuestion, UPLOAD_FOLDER): 

    # Get question_text and example_text
    question_text = request.form['questionInput']     
    example_text = request.form['explanationInput']   

    # Get users id (faculty who created the question)
    user_id = session.get('users_id')

    # Start connection
    cnx = makeConnection()
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

    return question_id

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpeg', 'jpg'} 

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS