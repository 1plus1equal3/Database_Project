var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

function getUserList(){
    fetch("http://localhost:5000/list_user")
      .then(response => response.json())
      .then(data => {
            console.log(data);
            generateUserList(data);
      })
}

function generateUserList(users){
    var mainContent = document.getElementById("content");
    users.forEach((user) => {
        var card = document.createElement("div");
        // Set class name for each card
        card.className = "card mb-4 py-3 border-left-primary";

        // Create an embedded link within the card
        var linkElement = document.createElement("a");
        linkElement.href = "http://localhost:5000/user_stats.html" + "?user_id=" + user.user_id;
        linkElement.style = "text-decoration: none; color: black;";

        var cardBody = document.createElement("div");
        // Customize cardBody content
        cardBody.className = "card-body d-flex align-items-center";
        cardBody.innerHTML = `
            <div class="ml-3">
                <strong>Student Name:</strong> ${user.username} <br>
                <strong>Student ID:</strong> ${user.user_id} <br>
                <strong>Student Email:</strong> ${user.email} <br>
            </div>
        `;

        linkElement.appendChild(cardBody);
        card.appendChild(linkElement);
        mainContent.appendChild(card);
    });
}