//================================================ GENERATE THE TEST
var selectedOptions = [];
var user_id = localStorage.getItem('user_id');
var test_id = getExamIdFromUrl();
var num_of_questions = 0;
var obj;
 
function generateQuestionList(questions) {
    var qbox = document.getElementById("questionbox");
    num_of_questions = questions.length;
    obj = {selectedOptions, user_id, test_id, num_of_questions};
    console.log(obj);
    questions.forEach((question, index) => {
        var card = document.createElement("div");
        card.className = "card shadow mb-4";

        var title = document.createElement("div");
        title.className = "card-header py-3";
        title.innerHTML = `<h6 class = "m-0 font-weight-bold text-primary">Question ${index + 1}</h6>`;

        var body = document.createElement("div");
        body.className = "card-body";
        var ques = document.createElement("p");
        ques.textContent = question.question;
        var choice1 = createChoice("first", "choice1", question.opt_a, index);
        var choice2 = createChoice("second", "choice2", question.opt_b, index);
        var choice3 = createChoice("third", "choice3", question.opt_c, index);
        var choice4 = createChoice("fourth", "choice4", question.opt_d, index);

        body.appendChild(ques);
        body.appendChild(choice1);
        body.appendChild(choice2);
        body.appendChild(choice3);
        body.appendChild(choice4);
 
        //Submit button for each question so as to save the selected choice
        var butt = document.createElement("button");
        butt.className = "btn btn-light btn-icon-split";
        butt.innerHTML = `
            <span class="icon text-gray-600">
                <i class="fas fa-arrow-right"></i>
                </span>
            <span class="text">Submit</span>
        `;

        butt.addEventListener('click', function() {
            var selectedOption = getSelectedOption(index);
            // Check if question_id is already in selectedOptions
            if (selectedOptions.some(e => e.question_id === question.question_id)) {
                // Update answer
                selectedOptions.forEach((option, index) => {
                    if (option.question_id === question.question_id) {
                        selectedOptions[index]['answer'] = selectedOption;
                    }
                });
            } else {
                selectedOptions.push({'answer': selectedOption, 'question_id': question.question_id}) // Store selected option in array
            }
            //finalAnswer = selectedOptions.map(jsonString => JSON.parse(jsonString));
            if (selectedOptions[index] !== null) {
                console.log("Question_id: " + question.question_id + " selected option: " + selectedOptions[index]['answer']);
            } else {
                console.log("No option selected for question " + index);
            }
            var box = document.getElementById(`box_${index+1}`);
            box.style.backgroundColor = "grey";
        });
        //console.log(typeof(selectedOptions))
        //console.log(typeof(JSON.stringify(selectedOptions)))

        var line = document.createElement("hr");
        line.className="new4";

        body.appendChild(butt);
        card.appendChild(title);
        card.appendChild(body);
        qbox.appendChild(card);
        qbox.appendChild(line);
    });
 
 
 
    //Submit test button
    var finalSubmitButton = document.createElement("button");
    finalSubmitButton.className = "btn btn-success btn-icon-split";
    finalSubmitButton.textContent = "Submit Test";
   finalSubmitButton.innerHTML = `
        <span class="icon text-white-50">
            <i class="fas fa-check"></i>
        </span>
        <span class="text">Submit Test</span>
   `;
     finalSubmitButton.addEventListener('click', function() {
    //     //testAssessment();
           console.log(selectedOptions)
           console.log(user_id)
           submitAnswer();
    //     // Call testAsssessment on final test submission
     });
 
    qbox.appendChild(finalSubmitButton);
 
    //SEND TO SERVER
   
    /*
    fetch('http://localhost:5000/test_interface', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(selectedOptions),
      })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Submit successfully');
                  //var newUrl = "dashboard_user.html";
                  //window.location = newUrl;
              } else {
                  alert('Submit fail');
              }
          })
          .catch((error) => {
              console.error('Error:', error);
          });
    */
 
}
 
 
function getExamIdFromUrl(){
    var url = new URL(window.location.href);
    test_id = url.searchParams.get("id");
    return test_id;
}
 
function loadQuestion() {
    var id = getExamIdFromUrl();
    console.log(id);
    var url = "http://localhost:5000/exam?exam_id=" + id;
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            generateQuestionList(data);
            generateProgressBox(data);
        });
}
 
 
function submitAnswer(){
    fetch('http://localhost:5000/submit_test', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(obj),
      })
     
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Submit successfully');
                  console.log('Submit state: ' + data.submit_state);
                  console.log('Point: ' + data.score + '/' + num_of_questions);
                  window.location = 'http://localhost:5000/dashboard_user.html'
              } else {
                  alert('Submit fail');
              }
          })
          .catch((error) => {
              console.error('Error:', error);
          });
         
}
 
 
 
function createChoice(id, labelFor, option, questionIndex) {
    var choice = document.createElement("div");
    choice.innerHTML = `
        <input type="radio" id="${id}" name="choice_${questionIndex}">
        <label for="${labelFor}">${option}</label>`;
    return choice;
}
 
function getSelectedOption(questionIndex) {
    var options = document.getElementsByName(`choice_${questionIndex}`);
    for (var i = 0; i < options.length; i++) {
        if (options[i].checked) {
            return i;
        }
    }
    return null; // If no option is selected
}
 
 
 
//================================================  GENERATE PROGRESS BOX
function generateProgressBox(questions) {
    var length = questions.length;
    var outbox = document.getElementById("outer");
    for (let i = 1; i <= length; i++) {
        var b = document.createElement("div");
        b.className = "content";
        b.innerHTML = i; // Display the value of i modulo 4
        b.id = `box_${i}`;
        outbox.appendChild(b); // Append the created div to the parent container
        if (i % 4 === 0) {
            // Create a line break after every fourth box
            outbox.appendChild(document.createElement("br"));
        }
    }
}
 
//================================================  SUBMIT THE TEST - TEST ASSESSMENT
function testAssessment() {
    //Load the true correct answer
    correctAnswers = [
        {
            opt_a: true,
            opt_b: false,
            opt_c: false,
            opt_d: false,
            question: "Title 1",
        },
        {
            opt_a: false,
            opt_b: true,
            opt_c: false,
            opt_d: false,
            question: "Title 2",
        },
        {
            opt_a: false,
            opt_b: true,
            opt_c: false,
            opt_d: false,
            question: "Title 2",
        },
        {
            opt_a: false,
            opt_b: true,
            opt_c: false,
            opt_d: false,
            question: "Title 2",
        },
        {
            opt_a: false,
            opt_b: true,
            opt_c: false,
            opt_d: false,
            question: "Title 2",
        },
        {
            opt_a: false,
            opt_b: true,
            opt_c: false,
            opt_d: false,
            question: "Title 2",
        },
        // Add corresponding correct answers here...
    ];
    showCorrectAnswer(correctAnswers);
}
 
function showCorrectAnswer(correctAnswers) {
    correctAnswers.forEach((answer, index) => {
        var options = document.getElementsByName(`choice_${index}`);
        for (var i = 0; i < options.length; i++) {
            var label = options[i].nextElementSibling;
            var box = document.getElementById(`box_${index+1}`);
            if(selectedOptions[index] == i) {
                if (answer[`opt_${String.fromCharCode(97 + i)}`]) {
                    box.style.backgroundColor = 'green';
                } else {
                    box.style.backgroundColor = 'red';
 
                }
            }
        }
    });
}