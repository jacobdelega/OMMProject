var currentIndex = 0; 
var questionStates = []; // this stores each selected answer and if correct or not

// JavaScript function to toggle visibility of question sets
function showQuestionSet(index) {
    var questionSets = document.getElementsByClassName('question-set');
    currentIndex = Math.min(Math.max(index, 0), questionSets.length - 1); // Ensure currentIndex is bounds. prevents index from going below 0, or over questionSets - 1

    for (var i = 0; i < questionSets.length; i++) {
        questionSets[i].style.display = i === currentIndex ? 'block' : 'none'; // if index i matches window.currentIndex make question set visible, else show none to hide
    }
    
    var currentState = questionStates[currentIndex] || {};

    // Set the selected answer if available
    var selectedAnswer = currentState.selectedAnswer;
    if (selectedAnswer) {
        document.querySelector('input[name="selected_answer"][value="' + selectedAnswer + '"]').checked = true;
    }

    clearFeedback();
}

function showFeedback() {
    var selectedAnswer = document.querySelector('input[name="selected_answer"]:checked');

    if (selectedAnswer) {
        var isCorrect = selectedAnswer.nextElementSibling.dataset.isCorrect;
        var feedbackContainer = document.querySelectorAll('.feedback-container')[currentIndex];

        if (feedbackContainer) {
            feedbackContainer.textContent = isCorrect === '1' ? 'You are correct!' : 'Incorrect.';
        }
    }
}

function clearFeedback() {
    var feedbackContainers = document.querySelectorAll('.feedback-container');
    var currentFeedbackContainer = feedbackContainers[currentIndex];

    if (currentFeedbackContainer) {
        // Only clear feedback if it was set during "Check work"
        if (!questionStates[currentIndex]?.movedToNext) {
            currentFeedbackContainer.textContent = '';
        }
    }
}

function storeAnswerData() {
    try {
        var selectedAnswer = document.querySelector('input[name="selected_answer"]:checked');

        if (selectedAnswer) {
            var isCorrect = selectedAnswer.nextElementSibling.dataset.isCorrect;

            var questionContainer = document.getElementsByClassName('question-set')[currentIndex];
            var questionID = questionContainer.dataset.questionId;

            questionStates[currentIndex] = {
                selectedAnswer: selectedAnswer.value,
                questionID: questionID,
                score: null,
                feedback: isCorrect === '1' ? 'Correct' : 'Incorrect'
            };
            console.log('questionStates:', questionStates); // This shows in Inspect -> console to view all data stored

            questionStates[currentIndex].movedToNext = true;
            // Move to the next question
            showQuestionSet(currentIndex + 1);
        }
    } catch (error) {
        console.error('Error in storeAnswerData:', error);
    }
}

function completeExam() {

    storeAnswerData();
    // Calculate the percentage of correct answers
    var correctCount = questionStates.filter(state => state.feedback === 'Correct').length;
    var totalQuestions = questionStates.length;
    var percentage = (correctCount / totalQuestions) * 100;
    console.log("percentage: " + percentage);
    //Store the score in questionSates
    questionStates[currentIndex].score = percentage.toFixed(0);

    // Loop through all questions to display feedback
    for (var i = 0; i < questionStates.length; i++) {
        var feedbackContainer = document.querySelectorAll('.feedback-container')[i];
        if (feedbackContainer) {
            feedbackContainer.textContent = questionStates[i].feedback || '';
        }
    }

    // Send the data to the Flask backend
    sendDataToFlask();

    alert('You completed the exam!\nPercentage Correct: ' + percentage.toFixed(0) + '%');
}

function sendDataToFlask() {
    const url = '/submit_data';

    const data = {
        questionStates: questionStates
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data sent successfully:', data);
    })
    .catch(error => {
        console.error('Error sending data:', error);
    });
}


function moveToPreviousQuestion() {
    clearFeedback();
    currentIndex = Math.max(currentIndex - 1, 0); // Move to the previous question index
    showQuestionSet(currentIndex); // Show the question set for the new index
}
