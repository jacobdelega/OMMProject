class testSet():

    def __init__(self):
        questionNumber = 0
        self.__testList = []

    def addQuestion(self, question):
        self.__testList.append(question)

    def getTestSet(self):
        return self.__testList
    