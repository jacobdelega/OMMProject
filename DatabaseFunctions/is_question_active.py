from database_connection import makeConnection

#Checks to see if question is active or not based on it's ID, 
# returns TRUE if is_active = 1, FALSE otherwise
def is_active(id):
    # Start connection
    cnx = makeConnection()
    cursor = cnx.cursor()

    #Gather a question that is active, it it exists then check will not equal NONE
    cursor.execute(f"SELECT question_text FROM question WHERE question_ID = {id} AND is_active = 1")
    check = cursor.fetchone()

    cnx.close()
    cursor.close()

    if check:
        return True
    return False