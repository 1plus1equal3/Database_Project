function generateExamList(exams) {
    var mainContent = document.getElementById("content");

    exams.forEach((exam) => {
        var card = document.createElement("div");
        // Set class name for each card
        card.className = "card mb-4 py-3 border-left-primary";

        var cardBody = document.createElement("div");
        // Customize cardBody content
        cardBody.className = "card-body";
        cardBody.innerHTML = `
            <h5 class="card-title">${exam.name}</h5>
            <p class="card-text">Question: ${exam.question}</p>
            <p class="card-text">Answer: ${exam.answer}</p>
        `;

        card.appendChild(cardBody);
        mainContent.appendChild(card);
    });
}

// use getExams() instead of generateExamList() in dashboard_user.html
// when call API to fetch real data

function getExams(){
    fetch("http://localhost:5000/request_exam")
      .then(response => response.json())
      .then(data => {
            console.log(data);
            generateExamList(data);
      })
}

generateExamList([
    {
        name: "name1",
        question: "question1",
        answer: "answer1",
    },
    {
        name: "name2",
        question: "question2",
        answer: "answer2",
    },
    {
        name: "name2",
        question: "question2",
        answer: "answer2",
    },
    {
        name: "name2",
        question: "question2",
        answer: "answer2",
    },
    {
        name: "name2",
        question: "question2",
        answer: "answer2",
    },
    {
        name: "name2",
        question: "question2",
        answer: "answer2",
    },
]);