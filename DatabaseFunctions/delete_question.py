from database_connection import makeConnection

# Give a question ID and this function will disable it in the database
def delete_question(ID):

    question_ID = ID

   # Start connection
    cnx = makeConnection()
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