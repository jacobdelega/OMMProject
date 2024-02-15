from Objects import Answer
import base64

class Question:

    #constructor with images
    def __init__(self, questionID, questionText, exampleText, answers, image, explanationImage):
        self.questionText = questionText 
        self.questionID = questionID  
        self.exampleText = exampleText                 
        self.answers = answers
        self.image = image
        self.explanationImage = explanationImage
        self.givenAnswer = None
        self.tags = []

    #constructor without images
    def __init__(self, questionID, questionText, exampleText, answers, UPLOAD_FOLDER):
        self.questionText = questionText 
        self.questionID = questionID  
        self.exampleText = exampleText                 
        self.answers = answers
        self.image = None
        self.explanationImage = None
        self.givenAnswer = None
        self.tags = []
        self.UPLOAD_FOLDER = UPLOAD_FOLDER

    #setters
    def setTags(self, tags):
        self.tags = tags

    def setQuestionText(self, questionText):
        self.questionText = questionText

    def setID(self, ID):
        self.ID = ID

    def setExampleText(self, exampleText):
        self.exampleText = exampleText

    def setAnswers(self, answers):
        self.answers = answers

    def setImage(self, image):
        self.image = image

    def setExplanationImage(self, image):
        self.explanationImage = image

    def setGivenAnswer(self, answer_id):
        self.givenAnswer = answer_id

    #getters
    def getQuestionText(self):
        return self.questionText
    
    def getID(self):
        return self.questionID
    
    def getAnswers(self):
        return self.answers
    
    def getExampleText(self):
        return self.exampleText
    
    def getTags(self):
        return self.tags

    def getImage(self):
        if (self.image is not None):
            pathToImage = self.UPLOAD_FOLDER + "/" + str(self.image)

            with open(pathToImage, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_string
        return None

    def getExplanationImage(self):
        if (self.explanationImage is not None):
            pathToImage = self.UPLOAD_FOLDER + "/" + str(self.explanationImage)

            with open(pathToImage, "rb") as explanation_image_file:
                encoded_string = base64.b64encode(explanation_image_file.read()).decode("utf-8")
            return encoded_string
        return None
    
    def getGivenAnswer(self):
        return self.givenAnswer
