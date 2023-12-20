import database_connection as dc


cnx = dc.makeConnection()

def getAttempts(cnx, user_id):

    cursor = cnx.cursor()
    query = (f"""select a.attempt_id, a.test_id, attempt_date, attempt_number, test_name
            from attempt a
            join test t on t.test_id = a.test_id
            where a.users_id = {user_id};""")

    cursor.execute(query)

    results = cursor.fetchall()

    attempts = []

    for result in results:
        attempts.append([result[0], result[1], str(result[2]), result[3], result[4]])

    cnx.close()

    return attempts