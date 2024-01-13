from DatabaseFunctions import get_question
from database_connection import makeConnection
from flask import redirect, render_template, request


def searchQuestions(UPLOAD_FOLDER):
    tagQuestions = []
    tag = ""
    if request.method == 'POST':
        if request.form['button'] == "idSearch":
            if request.form['searchQuestionID']:
                question_id = request.form.get('searchQuestionID')
                question = get_question.getquestionfromdatabase(int(question_id), UPLOAD_FOLDER)
                return redirect((f'/editQuestion/{question_id}'))
            
        if request.form['button'] == "tagSearch":
          tag = request.form.get('tagDropdown')
    
          #tagQuestions is a list of question dictionaries containing questionID, questionText, and tag
          tagQuestions = getQuestionListByTag(tag)
 
          #Passes the question list to searchQuestions.html 
          return render_template('searchQuestion.html', tagQuestions = tagQuestions, tag = tag)
    return render_template('searchQuestion.html', tagQuestions = tagQuestions, tag=tag)



# Give a tag and the function will return all the questions that have that tag
def getQuestionListByTag(tag):
    
    # Start connection
    cnx = makeConnection()
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

     #Close connection
    cnx.close()
    cursor.close()

    return questions
