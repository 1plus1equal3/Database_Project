function generateQuestionList(questions) {
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
