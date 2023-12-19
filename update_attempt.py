from datetime import time
import database_connection as dc

# This function inserts the score, if the attempt is complete, and total time taken
# for a finished attempt.
def updateAttempt(cnx, attempt_id, score, is_complete, time_taken):
    cursor = cnx.cursor()
    score = int(score)
    # print("Score:", score)
    # print("is_complete:", is_complete)
    # print("time_taken:", time_taken)
    # print("attempt_id:", attempt_id)

    update_attempt_query = (f"""update attempt
                            set score = {score}, is_complete = {is_complete}, time_taken = {time_taken}
                            where attempt_id = {attempt_id}""")

    cursor.execute(update_attempt_query)
    cnx.commit()
    cnx.close()