var currentIndex = 0; 
var questionStates = []; // this stores each selected answer and if correct or not
let timerInterval;
let seconds = 0;
let minutes = 0;
let timerStopped = false;

function startTimer() {
    timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
    timerStopped = true;
}

function padNumber(number) {
    return number < 10 ? '0' + number : number;
}

function updateTimer() {
    seconds++;
    if (seconds === 60) {
        seconds = 0;
        minutes++;
    }
    const formattedTime = `${padNumber(minutes.toString())}:${padNumber(seconds.toString())}`;
    document.getElementById('timer').innerText = formattedTime;
}

// JavaScript function to toggle visibility of question sets
function showQuestionSet(index) {
    var questionSets = document.getElementsByClassName('question-set');
    currentIndex = Math.min(Math.max(index, 0), questionSets.length - 1); // Ensure currentIndex is bounds. prevents index from going below 0, or over questionSets - 1

    for (var i = 0; i < questionSets.length; i++) {
        questionSets[i].style.display = i === currentIndex ? 'block' : 'none'; // if index i matches window.currentIndex make question set visible, else show none to hide
    }
    
    var currentState = questionStates[currentIndex] || {};
    var exampleContainer = document.querySelectorAll('.example-container')[i];

    // Show example text if available
    if (exampleContainer) {
        exampleContainer.style.display = currentState.exampleShown ? 'block' : 'none';
    }
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
            showExampleText();
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
                time: null,
                feedback: isCorrect === '1' ? '1' : '0',
                feedbackText: isCorrect === '1' ? 'You are correct!' : 'Incorrect.'
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
    var correctCount = questionStates.filter(state => state.feedback === '1').length;
    var totalQuestions = questionStates.length;
    var percentage = (correctCount / totalQuestions) * 100;

    //Store the score in questionSates
    questionStates[currentIndex].score = percentage.toFixed(0);

    // Set exampleShown to true for all questions when exam is complete
    for (var i = 0; i < questionStates.length; i++) {
        questionStates[i].exampleShown = true;
    }
    // Loop through all questions to display feedback
    for (var i = 0; i < questionStates.length; i++) {
        var feedbackContainer = document.querySelectorAll('.feedback-container')[i];
        if (feedbackContainer) {
            feedbackContainer.textContent = questionStates[i].feedback || '';
            showExampleText();
        }
    }

    stopTimer();

    const totalTimeInSeconds = (minutes * 60) + seconds;
    //Store the score in questionSates
    questionStates[currentIndex].time = totalTimeInSeconds

    // Send the data to the Flask backend
    sendDataToFlask();
    
    alert('You completed the exam!\nPercentage Correct: ' + percentage.toFixed(0) + '%');

    window.location.href = '/testResult';
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

function exitExam() {
    storeAnswerData(); // Store the current state before exiting
    sendDataToFlask(); // Send the data to the Flask backend

    // Optionally, you can redirect the user or perform any other actions
    alert('You exited the exam!');
    window.location.href = '/home';
}

function moveToPreviousQuestion() {
    clearFeedback();
    currentIndex = Math.max(currentIndex - 1, 0); // Move to the previous question index
    showQuestionSet(currentIndex); // Show the question set for the new index
}

// Function to handle highlighting selected answer
function highlightSelectedText() {
    if (window.getSelection) {
        const selection = window.getSelection();
        if (selection.toString().length > 0) {
            const range = selection.getRangeAt(0);
            const span = document.createElement('span');
            span.className = 'highlighted-text';
            span.appendChild(range.extractContents());
            range.insertNode(span);
        }
    }
}

// Function to handle striking through selected answer
function strikethroughSelectedAnswer() {
    let selectedAnswer = document.querySelector('input[name="selected_answer"]:checked + label');
    if (selectedAnswer) {
        selectedAnswer.classList.toggle('strikethrough');
        selectedAnswer.previousElementSibling.disabled = true; // Disable the selected answer
    }
}

function moveToNextQuestion() {
    clearFeedback();
    currentIndex = Math.max(currentIndex + 1, 0); // Move to the previous question index
    showQuestionSet(currentIndex); // Show the question set for the new index
}

function moveToPreviousQuestion() {
    clearFeedback();
    currentIndex = Math.max(currentIndex - 1, 0); // Move to the previous question index
    showQuestionSet(currentIndex); // Show the question set for the new index
}

function showExampleText() {
    var exampleContainer = document.querySelectorAll('.example-container')[currentIndex];
    if (exampleContainer) {
        exampleContainer.style.display = 'block';
    }
}
function exitViewAttempt() {

    window.location.href = '/home';
}
