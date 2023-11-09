class testSet():

    def __init__(self):
        self.__questionNumber = 0
        self.__testList = []

    def addQuestion(self, question):
        self.__questionNumber += 1
        self.__testList.append(question)

    def getTestSet(self):
        return self.__testList
    