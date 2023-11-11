class Answer:
    
    def __init__(self, answerText, isCorrect):
        self.answerText = answerText
        self.isCorrect = isCorrect

    #setters
    def setAnswerText(self, answerText):
        self.answerText = answerText

    def setIsCorrect(self, isCorrect):
        self.isCorrect = isCorrect

    #getters
    def getAnswerText(self):
        return self.answerText

    def getIsCorrect(self):
        return self.isCorrect
