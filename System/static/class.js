function generateClassList(Class_list) {
        var container = document.getElementById("content");
        // Iterate over each JSON object and create card elements
        Class_list.forEach(function (item, index) {
            // Create a new card element
            var cardElement = document.createElement("div");
            cardElement.className = "card mb-4 py-3 border-left-primary"; // You can customize the classes here
            cardElement.id = "exam_" + (index + 1); // Generate a unique ID for each card

            // Create the card body
            var cardBodyElement = document.createElement("div");
            cardBodyElement.className = "card-body d-flex align-items-center"; // Ensure content is vertically centered

            // Create an embedded link within the card
            var linkElement = document.createElement("a");
            linkElement.href = "class_interface.html" + "?id="
            linkElement.style = "text-decoration: none; color: black;";

            cardBodyElement.innerHTML += `
                <div class="ml-3">
                    <strong>Class Name:</strong> ${item.title} <br>
                    <strong>Date Created:</strong> ${item.date} <br>
                    <strong>Number of students:</strong> ${item.std_num}<br>
                </div>
      `     ;

            // Append the card body to the link
            linkElement.appendChild(cardBodyElement);

            // Append the link to the card
            cardElement.appendChild(linkElement);

            // Append the card to the container
            container.appendChild(cardElement);
    });
}

// use getExams() instead of generateExamList() in dashboard_user.html
// when call API to fetch real data

function getClass(){
    user_id = localStorage.getItem("user_id");
    fetch("http://localhost:5000/request_class" + "?id=" + user_id)
      .then(response => response.json())
      .then(data => {
            console.log(data);
            generateClassList(data);
      })
    user_name = document.getElementById("username");  
    user_name.innerHTML = localStorage.getItem("username");
    profile = document.getElementById("profile_url");
    profile.href = "http://localhost:5000/profile_admin.html"
}

