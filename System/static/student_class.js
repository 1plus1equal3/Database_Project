var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

var currentPage = 0;
var itemPerPage = 12;
var class_list = [];

init();

function generateClassList(Class_list) {
    var container = document.getElementById("content");
    // Clear the container
    container.innerHTML = '';
    // Iterate over each JSON object and create card elements
    Class_list.forEach(function (item, index) {
        if (index >= itemPerPage * currentPage && index < itemPerPage * (currentPage + 1)) {
            // Create a new card element
            var cardElement = document.createElement("div");
            cardElement.className = "card mb-4 py-3 border-left-primary"; // Customize the classes here
            cardElement.id = "exam_" + (index + 1); // Generate a unique ID for each card
            // Create the card body
            var cardBodyElement = document.createElement("div");
            cardBodyElement.className = "card-body d-flex align-items-center"; // Ensure content is vertically centered
            // Create an embedded link within the card
            var linkElement = document.createElement("a");
            linkElement.href = "user_class.html?id=" + item.id; // Append the ID correctly
            linkElement.style = "text-decoration: none; color: black;";
            cardBodyElement.innerHTML = `
                <div class="ml-3">
                    <strong>Class:</strong> ${item.title} <br>
                    <strong>Date Created:</strong> ${item.create_date} <br>
                    <strong>Teacher:</strong> ${item.teacher} <br>
                </div>`;
            // Append the card body to the link
            linkElement.appendChild(cardBodyElement);
            // Append the link to the card
            cardElement.appendChild(linkElement);
            // Append the card to the container
            container.appendChild(cardElement);
        }
    });
}

function getPageCount(class_list) {
    if (!class_list || class_list.length === 0) {
        return 0; // Return 0 if class_list is undefined or empty
    }
    return Math.ceil(class_list.length / itemPerPage);
}

function previousPage(class_list) {
    if (currentPage > 0) {
        currentPage--;
        generateClassList(class_list);
        console.log(currentPage);
    } else {
        console.log("You are on the first page");
    }
}

function nextPage(class_list) {
    var totalPages = getPageCount(class_list);
    console.log("Next page button pressed");
    console.log("Total page:", totalPages);
    console.log("Current page:", currentPage);
    if (totalPages < 0) {
        console.log("No items in the class list");
        return;
    }
    if (currentPage < totalPages - 1) {
        currentPage++;
        generateClassList(class_list);
        console.log(currentPage);
    } else {
        console.log("You are on the last page");
    }
}

function firstPage(class_list) {
    if (currentPage !== 0) {
        currentPage = 0;
        generateClassList(class_list);
        console.log("Navigated to first page");
    }
}

function lastPage(class_list) {
    var totalPages = getPageCount(class_list);
    if (currentPage !== totalPages - 1) {
        currentPage = totalPages - 1;
        generateClassList(class_list);
        console.log("Navigated to last page");
    }
}
// Sample data for demonstration
// const class_list = [
//     { name: "name1", ID: "question1" },
//     { name: "name2", ID: "question2" },
//     { name: "name3", ID: "question3" },
//     { name: "name4", ID: "question4" },
//     { name: "name5", ID: "question5" },
//     { name: "name6", ID: "question6" },
//     { name: "name7", ID: "question7" },
//     { name: "name8", ID: "question8" },
//     { name: "name9", ID: "question9" },
//     { name: "name10", ID: "question10" },
//     { name: "name11", ID: "question11" },
//     { name: "name12", ID: "question12" },
//     { name: "name13", ID: "question13" },
//     { name: "name14", ID: "question14" },
//     { name: "name15", ID: "question15" },
//     { name: "name16", ID: "question16" },
//     { name: "name17", ID: "question17" },
//     { name: "name18", ID: "question18" },
//     { name: "name19", ID: "question19" },
//     { name: "name20", ID: "question20" },
//     { name: "name21", ID: "question21" },
//     { name: "name22", ID: "question22" },
//     { name: "name23", ID: "question23" },
//     { name: "name24", ID: "question24" },
//     { name: "name25", ID: "question25" },
//     { name: "name26", ID: "question26" },
//     { name: "name27", ID: "question27" },
//     { name: "name28", ID: "question28" },
//     { name: "name29", ID: "question29" },
//     { name: "name30", ID: "question30" },
//     { name: "name31", ID: "question31" },
//     { name: "name32", ID: "question32" },
//     { name: "name33", ID: "question33" },
//     { name: "name34", ID: "question34" },
//     { name: "name35", ID: "question35" },
//     { name: "name36", ID: "question36" },
//     { name: "name37", ID: "question37" },
//     { name: "name38", ID: "question38" },
//     { name: "name39", ID: "question39" },
//     { name: "name40", ID: "question40" },
//     { name: "name41", ID: "question41" },
//     { name: "name42", ID: "question42" },
//     { name: "name43", ID: "question43" },
//     { name: "name44", ID: "question44" },
//     { name: "name45", ID: "question45" },
//     { name: "name46", ID: "question46" },
//     { name: "name47", ID: "question47" },
//     { name: "name48", ID: "question48" },
//     { name: "name49", ID: "question49" },
//     { name: "name50", ID: "question50" },
// ];

// Initial render
function init() {
    // Fetch class list from the server
    fetch("http://localhost:5000/student_class?id=" + localStorage.getItem('user_id'), {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            class_list = data;
            generateClassList(class_list);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

// Event listeners for navigation buttons
document.getElementById("prevBtn").addEventListener("click", function() {
    previousPage(class_list);
});

document.getElementById("nextBtn").addEventListener("click", function() {
    nextPage(class_list);
});

document.getElementById("firstBtn").addEventListener("click", function() {
    firstPage(class_list);
});

document.getElementById("lastBtn").addEventListener("click", function() {
    lastPage(class_list);
});
