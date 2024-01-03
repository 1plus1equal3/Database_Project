function createExamDiv(jsonData){
    var container = document.getElementById("content");

  // Iterate over each JSON object and create card elements
  jsonData.forEach(function(item, index) {
    // Create an embbeded link
    var linkElement = document.createElement("a");
    linkElement.href = "test_interface.html" + "?id=" + item.exam_id;
    linkElement.style = "text-decoration: none; color: black;";
    // Create a new card element
    var cardElement = document.createElement("div");
    cardElement.className = "card mb-4 py-3 border-left-primary"; // You can customize the classes here
    cardElement.id = "exam_" + (index + 1); // Generate a unique ID for each card

    // Create the card body
    var cardBodyElement = document.createElement("div");
    cardBodyElement.className = "card-body";
    cardBodyElement.innerHTML = `
      <strong>Title:</strong> ${item.title} <br>
      <strong>Date Created:</strong> ${item.date_created} <br>
    `;

    // Append the card to the link
    linkElement.appendChild(cardBodyElement);
    // Append the card body to the card
    cardElement.appendChild(linkElement);
    // Append the card to the container
    container.appendChild(cardElement);
  });
}

function loadQuestion(){
    fetch('http://localhost:5000/request_exam', {
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