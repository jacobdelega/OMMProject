#This Test Set is an arrayList of all the questions queried from the database
import Question

class testSet():
    def __init__(self):
        self.__amtOfQuestions = 0
        self.__testList = []
        self.__currentQuestion = 0

    #Returns the amount of questions in the list
    def length(self):
        return self.__amtOfQuestions
    
    #Adds a question to the test list
    def addQuestion(self, question):
        self.__amtOfQuestions += 1
        self.__testList.append(question)


    #Returns the whole test set, if needed
    def getTestSet(self): 
        return self.__testList
    
    # #Increments the question location & returns that question
    def getNextQuestion(self):
        if(self.__currentQuestion < self.__amtOfQuestions):
            self.__currentQuestion += 1

        return self.__testList[self.__currentQuestion]
    
    #returns the current question
    def getCurrentQuestion(self):
        return self.__testList[self.__currentQuestion]


    #Decrements the question location & returns the previous question
    def getPrevQuestion(self):
        if self.__currentQuestion > 0:
            self.__currentQuestion -= 1

        return self.__testList[self.__currentQuestion]

    #Goes to a specific question in the list, and returns that question
    def getQuestionAtLocation(self, location):
        self.__currentQuestion = location 

        return self.__testList[self.__currentQuestion]

        