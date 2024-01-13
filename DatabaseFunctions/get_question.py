from database_connection import makeConnection
import os
from Objects import Answer, Question



# Give a question_ID and it will return that question in a Question object
def getquestionfromdatabase(ID, UPLOAD_FOLDER):

    # Start connection
    cnx = makeConnection()
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
    question = Question.Question(return_value[0][0], return_value[0][1], return_value[0][2], answer_objects, UPLOAD_FOLDER)

    question_id = question.getID()

    # creating the names for what images to get for a specific question id
    filenameImage = 'question_' + str(question_id) + '.jpeg'
    filenameExplanationImage = 'question_' + str(question_id) + '_explanation.jpeg'
    pathToImage = UPLOAD_FOLDER + "/" + filenameImage
    pathToExplanationImage = UPLOAD_FOLDER + "/" + filenameExplanationImage

    # store image to question
    if os.path.isfile(pathToImage):
        print("Successfully added image to question")
        question.setImage(filenameImage)
        print(filenameImage)
    else:
        print("Failed to add image to question, question ID: ")
        print(question_id)

    # store explanation image to question
    if os.path.isfile(pathToExplanationImage):
        print("Successfully added image to explanation")
        question.setExplanationImage(filenameExplanationImage)  
        print(filenameExplanationImage)
    else:
        print("Failed to add image to explanation, question ID: ")
        print(question_id)


    #Getting question tags from database
    tags = []
    cursor.execute('''Select t.tag_name from tag_question as tq 
        LEFT JOIN tag as t on tq.tag_ID=t.tag_ID
        WHERE tq.question_ID = %s;''', (question_id, )) #returns a list of tag_names from the database
    for tag in cursor.fetchall():
        tags.append(tag[0])
    
    question.setTags(tags)

    #Close connection
    cnx.close()
    cursor.close()

    return question