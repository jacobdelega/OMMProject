import Answer

class Question:

    #constructor
    def __init__(self, questionID, questionText, exampleText, answers):
        self.questionText = questionText 
        self.questionID = questionID  
        self.exampleText = exampleText                 
        self.answers = answers

    #setters
    def setQuestionText(self, questionText):
        self.questionText = questionText

    def setID(self, ID):
        self.ID = ID
    
    def setAnswers(self, answers):
        self.answers = answers

    def setExampleText(self, exampleText):
        self.exampleText = exampleText

    def setAnswers(self, answers):
        self.answersSQL = answers.split(", ")
        self.answers = []
        index = 0
        for i in self.answersSQL:
            self.answersSQL[index] = i.strip("[]") 
            self.answers.append(Answer.Answer(self.answersSQL[index].split(":")[0], self.answersSQL[index].split(":")[1]))
            index += 1

    #getters
    def getQuestionText(self):
        return self.questionText
    
    def getID(self):
        return self.questionID
    
    def getAnswers(self):
        return self.answers
    
    def getExampleText(self):
        return self.exampleText