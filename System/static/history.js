var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

function generateHistoryList(exams) {
    var mainContent = document.getElementById("content");

    exams.forEach((exam) => {
        var card = document.createElement("div");
        // Set class name for each card
        card.className = "card mb-4 py-3 border-left-primary";

        var cardBody = document.createElement("div");
        // Customize cardBody content
        cardBody.className = "card-body";
        cardBody.innerHTML = `
            <h5 class="card-title">${exam.title}</h5>
            <p class="card-text">Score: ${exam.score}</p>
            <p class="card-text">Date: ${exam.date}</p>
        `;

        card.appendChild(cardBody);
        mainContent.appendChild(card);
    });
}

// use getExams() instead of generateExamList() in dashboard_user.html
// when call API to fetch real data

function getUserHistory(){
    user_id = localStorage.getItem("user_id");
    fetch("http://localhost:5000/history?user_id=" + user_id)
      .then(response => response.json())
      .then(data => {
            console.log(data);
            generateHistoryList(data);
      })
}
