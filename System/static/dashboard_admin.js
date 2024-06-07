var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

function createExamDiv(jsonData) {
  var container = document.getElementById("content");

  // Iterate over each JSON object and create card elements
  jsonData.forEach(function (item, index) {
      // Create a new card element
      var cardElement = document.createElement("div");
      cardElement.className = "card mb-4 py-3 border-left-primary"; // You can customize the classes here
      cardElement.id = "exam_" + (index + 1); // Generate a unique ID for each card

      // Create the card body
      var cardBodyElement = document.createElement("div");
      cardBodyElement.className = "card-body d-flex align-items-center"; // Ensure content is vertically centered

      // Create an embedded link within the card
      var linkElement = document.createElement("a");
      linkElement.href = "http://localhost:5000/test_view.html" + "?id=" + item.exam_id;
      linkElement.style = "text-decoration: none; color: black;";

      // Create an image representation inside the card body
      var image = document.createElement("img");
      image.src = "/static/course.png";
      image.width = "100";
      image.height = "100";
      difficulty = 'Easy';
      if(item.difficulty == 2){
        difficulty = 'Medium';
      }else if(item.difficulty == 3){
        difficulty = 'Hard';
      }
      subject = item.subject;
      if(subject == null) subject = 'Multiple Subjects';
      
      // Add exam details to the card body
      cardBodyElement.appendChild(image);
      cardBodyElement.innerHTML += `
          <div class="ml-3">
              <strong>Title:</strong> ${item.title} <br>
              <strong>Subject:</strong> ${subject} <br>
              <strong>Difficulty:</strong> ${difficulty} <br>
          </div>
      `;

      // Append the card body to the link
      linkElement.appendChild(cardBodyElement);

      // Append the link to the card
      cardElement.appendChild(linkElement);

      // Append the card to the container
      container.appendChild(cardElement);
  });
}

function loadQuestion(){
    fetch('http://localhost:5000/request_admin_exam' + '?id=' + localStorage.getItem('user_id'), {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      })
      .then(response => response.json())
      .then(data => {
            console.log(data);
            createExamDiv(data);
      })
}
