function generateQuestionList(questions) {
    /*
    var qbox = document.getElementById("questionbox");
    var i = 0;
    questions.forEach(question => {
        var card = document.createElement("div");
        card.className = "question";

        var body = document.createElement("div");
        body.className = "choice";
        body.innerHTML = `<p>${question.question}</p>`;

        var choice1 = document.createElement("div");
        choice1.innerHTML = `
            <input type="radio" id="first" name=question_${i}>
            <label for="choice1">${question.opt_a}</label>`;
        body.appendChild(choice1);

        var choice2 = document.createElement("div");
        choice2.innerHTML = `
            <input type="radio" id="second" name=question_${i}>
            <label for="choice2">${question.opt_b}</label>`;
        body.appendChild(choice2);

        var choice3 = document.createElement("div");
        choice3.innerHTML = `
            <input type="radio" id="third" name=question_${i}>
            <label for="choice3">${question.opt_c}</label>`;
        body.appendChild(choice3);

        var choice4 = document.createElement("div");
        choice4.innerHTML = `
            <input type="radio" id="fourth" name=question_${i}>
            <label for="choice4">${question.opt_d}</label>`;
        body.appendChild(choice4);

        var butt = document.createElement("button");
        butt.textContent = "Submit";
        body.appendChild(butt);

        card.appendChild(body);
        qbox.appendChild(card);
        i++;
    });
    */

    var qbox = document.getElementById("questionbox");
    questions.forEach((question, index) => {
        var card = document.createElement("div");
        card.className = "question";

        var body = document.createElement("div");
        body.className = "choice";
        body.innerHTML = `<p>${question.question}</p>`;

        var choice1 = createChoice("first", "choice1", question.opt_a, index);
        var choice2 = createChoice("second", "choice2", question.opt_b, index);
        var choice3 = createChoice("third", "choice3", question.opt_c, index);
        var choice4 = createChoice("fourth", "choice4", question.opt_d, index);

        body.appendChild(choice1);
        body.appendChild(choice2);
        body.appendChild(choice3);
        body.appendChild(choice4);

        var butt = document.createElement("button");
        butt.textContent = "Submit";
        butt.addEventListener('click', function() {
            var selectedOption = getSelectedOption(index);
            if (selectedOption !== null) {
                console.log("Question " + index + " selected option: " + selectedOption);
            } else {
                console.log("No option selected for question " + index);
            }
        });

        body.appendChild(butt);
        card.appendChild(body);
        qbox.appendChild(card);
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

function generateProgressBox(questions) {
    var length = questions.length;
    var outbox = document.getElementById("outer");
    for (let i = 1; i <= length; i++) {
        var b = document.createElement("div");
        b.className = "content";
        b.innerHTML = i; // Display the value of i modulo 4
        outbox.appendChild(b); // Append the created div to the parent container
        if (i % 4 === 0) {
            // Create a line break after every fourth box
            outbox.appendChild(document.createElement("br"));
        }
    }
}


function getExamIdFromUrl(){
    var url = new URL(window.location.href);
    var id = url.searchParams.get("id");
    return id;
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


function loadBox() {
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
            generateProgressBox(data);
        });
}

// generateQuestionList([
//     {
//         opt_a: "A",
//         opt_b: "B",
//         opt_c: "C",
//         opt_d: "D",
//         question: "Title",
//     },
//     {
//         opt_a: "A",
//         opt_b: "B",
//         opt_c: "C",
//         opt_d: "D",
//         question: "Title",
//     },
//     {
//         opt_a: "A",
//         opt_b: "B",
//         opt_c: "C",
//         opt_d: "D",
//         question: "Title",
//     },
//     {
//         opt_a: "A",
//         opt_b: "B",
//         opt_c: "C",
//         opt_d: "D",
//         question: "Title",
//     },
//     {
//         opt_a: "A",
//         opt_b: "B",
//         opt_c: "C",
//         opt_d: "D",
//         question: "Title",
//     },
// ]);
