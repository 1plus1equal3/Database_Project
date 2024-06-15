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
      const id = window.location.search.split("=")[1];
      var linkElement = document.createElement("a");
      linkElement.href = "test_interface.html" + "?id=" + item.test_id + "&class_id=" + id;
      linkElement.style = "text-decoration: none; color: black;";

      // Create an image representation inside the card body
      var image = document.createElement("img");
      image.src = "/static/course.png";
      image.width = "100";
      image.height = "100";

      // Add exam details to the card body
      cardBodyElement.appendChild(image);
      cardBodyElement.innerHTML += `
          <div class="ml-3">
              <strong>Title:</strong> ${item.title} <br>
              <strong>Subject:</strong> ${item.subject} <br>
              <strong>Duration:</strong> ${item.duration} <br>
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
    const id = window.location.search.split("=")[1];
    fetch('http://localhost:5000/get_class_test?id=' + id, {
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
