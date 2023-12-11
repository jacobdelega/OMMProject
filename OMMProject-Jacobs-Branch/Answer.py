class Answer:
    
    def __init__(self, answerID, answerText, isCorrect):
        self.answerText = answerText
        self.isCorrect = isCorrect
        self.answerID = answerID


    #setters
    def setAnswerText(self, answerText):
        self.answerText = answerText

    def setIsCorrect(self, isCorrect):
        self.isCorrect = isCorrect

    def setAnswerID(self, answerID):
        self.answerID = answerID

    #getters
    def getAnswerText(self):
        return self.answerText

    def getIsCorrect(self):
        return self.isCorrect

    def getAnswerID(self):
        return self.answerID
