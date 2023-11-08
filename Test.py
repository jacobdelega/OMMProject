import Question
import Answer

var = Question.Question(4, "Name all the different bones in the leg?", "There are blah blah bones in the body", "[answer1:1], [legs:0], [cpr: 0]")

# print(var.getQuestionText())
# print(var.getAnswers())
# print(var.getExampleText())
# print(var.getID())

var2 = var.getAnswers()

print(var2[0].getAnswerText())
print(var2[0].getIsCorrect())

var.setAnswers("[banana:0], [bionicle:1], [random: 0]")

var3 = var.getAnswers()
print(var3[0].getAnswerText())
print(var3[0].getIsCorrect())

print(var3[1].getAnswerText())
print(var3[1].getIsCorrect())





