import Answer, Question, testSet
import mysql.connector


def connectDataBase():
    return mysql.connector.connect(
        host = '3.87.120.222',
        user='delega25',
        password='OMMProject',
        database='omm'
    )

def getTest(test_id):
    cursor = connectDataBase.cursor()
    test_set = testSet.testSet()

    query = (f"""select q.question_ID, question_text, example_text, GROUP_CONCAT(CONCAT( "[", answer_text, ":", is_correct, "]")) as answers
                from question q
                join question_answer qa on qa.question_ID = q.question_ID
                join answer a on a.answer_ID = qa.answer_ID
                join test_question tq on tq.question_ID = q.question_ID
                join test t on t.test_ID = tq.test_ID
                where t.test_ID = {test_id} and is_active = 1
                group by q.question_ID, question_text, example_text;""")

    cursor.execute(query)

    for result in cursor.fetchall():

        answer_objects = []
        answers  = result[3].replace("],[", "]|[").split("|")

        for answer in answers:
            text = answer[1:-1].split(":")[0]
            is_correct = answer[1:-1].split(":")[1]
        
            answer = Answer.Answer(text, is_correct)
            answer_objects.append(answer)

        question = Question.Question(result[0], result[1], result[2], answer_objects)

        test_set.addQuestion(question)

    return test_set