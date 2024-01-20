var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

// admin_search_question.js

function addQuestionToGrid(questionData) {
    // Create a new card element
    var cardElement = document.createElement("div");
    cardElement.className = "card"; // You can customize the classes here
    cardElement.id = "question_info";
    
    // Create the card body
    var cardBodyElement = document.createElement("div");
    cardBodyElement.className = "card-body align-items-center";

    // Create the HTML content for the question using the provided data
    var questionHTML = "<p><strong>Question ID:</strong> " + questionData.question_id + "</p>" +
                       "<p><strong>Content:</strong> " + questionData.content + "</p>" +
                       "<p><strong>Level:</strong> " + questionData.level + "</p>" +
                       "<p><strong>Subject:</strong> " + questionData.subject + "</p>" +
                       "<p><strong>Options:</strong> A: " + questionData.opt_a +
                       ", B: " + questionData.opt_b + ", C: " + questionData.opt_c +
                       ", D: " + questionData.opt_d + "</p>";

    var questionHTML = `<div class="card-text">
    <strong>Question ID:</strong> ${questionData.question_id} <br>
    <strong>Content:</strong> ${questionData.content} <br>
    <strong>Level:</strong> ${questionData.level} <br>
    <strong>Subject:</strong> ${questionData.subject} <br>
    <strong>Options:</strong> <br>
    A: ${questionData.opt_a} <br>
    B: ${questionData.opt_b} <br>
    C: ${questionData.opt_c} <br>
    D: ${questionData.opt_d} <br>
</div>`
    // Add the HTML content to the card body
    cardBodyElement.innerHTML = questionHTML;
    cardElement.appendChild(cardBodyElement);

    // Append the question div to the searchContent div
    document.getElementById("content_t").appendChild(cardElement);
}


function createQuestionList(jsonData) {
    // Clear the question elements
    child = document.getElementById("question_info");
    while (child != null) {
        child.parentNode.removeChild(child);
        child = document.getElementById("question_info");
    }

    // For each question in the JSON data, add it to the grid
    jsonData.forEach(addQuestionToGrid);
}

function loadSearchQuestion(body){
    fetch('http://localhost:5000/search_question', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
      })
      .then(response => response.json())
      .then(data => {
            console.log(data);
            createQuestionList(data);
      })
}

function executeSearch() {
    var searchba = document.getElementById("searchBar");
    var searching = searchba.value;
    var subject = document.getElementById('subject').value;
    var difficulty = document.getElementById('difficulty').value;
    var searchObject = {
        search: searching,
        subject: subject,
        difficulty: difficulty
    }
    console.log(searchObject);
    loadSearchQuestion(searchObject);
}
