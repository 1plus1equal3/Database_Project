var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;
var currentPage = 0;
var itemPerPage = 7;
var selectedclass = [];
var class_list = [];
getClass();

// Display the class's list
function AddTable(class_list) {
    var tableBody = document.getElementById("dataTableBody");
    tableBody.innerHTML = ''; // Clear existing rows

    class_list.forEach(function (c, index) {
        if (index >= itemPerPage * currentPage && index < itemPerPage * (currentPage + 1)) {
            var newRow = AddRow(index + 1, c.title, c.id);
            tableBody.appendChild(newRow);
        }
    });
}

function AddRow(no, name, id) {
    var row = document.createElement("tr");

    var no_cell = document.createElement("td");
    no_cell.textContent = no;
    row.appendChild(no_cell);

    var name_cell = document.createElement("td");
    name_cell.textContent = name;
    row.appendChild(name_cell);

    var id_cell = document.createElement("td");
    id_cell.textContent = id;
    row.appendChild(id_cell);

    var delete_cell = document.createElement("td");
    var delete_checkbox = document.createElement("input");

    // Set the checkbox type and value
    delete_checkbox.type = "checkbox";
    // Check if the ID is already in the selectedclass array and set the checkbox state accordingly
    console.log(selectedclass);
    if (selectedclass.includes(id.toString())) {
        delete_checkbox.checked = true;
    } else {
        delete_checkbox.checked = false;
    }
    // Set value as class ID for identification
    delete_checkbox.value = id; 

    // Add an event listener for the change event
    delete_checkbox.addEventListener("change", function() {
        if (delete_checkbox.checked) {
            // If the checkbox is checked, add the ID to the selectedclass array
            selectedclass.push(delete_checkbox.value);
            console.log(selectedclass);
        } else {
            // If the checkbox is unchecked, remove the ID from the selectedclass array
            const index = selectedclass.indexOf(delete_checkbox.value);
            selectedclass.splice(index, 1);
            console.log(selectedclass);
        }
    });

    delete_cell.appendChild(delete_checkbox);
    row.appendChild(delete_cell);

    return row;
}

function getPageCount(class_list) {
    if (!class_list || class_list.length === 0) {
        return 0;
    }
    return Math.ceil(class_list.length / itemPerPage);
}

function previousPage(class_list) {
    if (currentPage > 0) {
        currentPage--;
        AddTable(class_list);
        console.log(selectedclass);
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
        AddTable(class_list);
        console.log(selectedclass);
    } else {
        console.log("You are on the last page");
    }
}

// Delete selected classs
function deleteSelected() {
    console.log("Selected classs:", selectedclass);
    // Send a DELETE request to the server
    fetch("http://localhost:5000/delete_class", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'class_ids': selectedclass}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.success){
            alert("Delete class successfully!");
            window.location.reload();
        }
        else alert("Delete class failed!");
    });
}

// Sample data for demonstration
// const class_list = [
//     { name: "Pham Quang Huy", id: "20215207" },
//     { name: "Tran Thuy Chau", id: "20215182" },
//     { name: "Nguyen Dang Duy", id: "20210272" },
//     { name: "Bui Duc Viet", id: "20215254" },
//     { name: "Hoang Van Khang", id: "20215182" },
//     { name: "Chu Xuan Minh", id: "20235527" },
//     { name: "Phan Ha Quyen", id: "20225224" },
//     { name: "Nguyen Manh Cuong", id: "202151844" },
//     { name: "Phan Dinh Trung", id: "20230093" },
//     { name: "Nguyen Hoang Viet", id: "20220050" },
//     { name: "Vu Thuong Tin", id: "20230091" },
//     { name: "Nguyen Thuy Anh", id: "20215306" },
//     { name: "Nguyen Cong Duy", id: "20215188" },
//     { name: "Do Hong Hai", id: "20215199" },
//     { name: "Tran Quang Hung", id: "20235502" },
//     { name: "Do Dang Vu", id: "20235578" }
// ];

// Initial render
//AddTable(class_list);
function getClass(){
    user_id = localStorage.getItem("user_id");
    fetch("http://localhost:5000/request_class" + "?id=" + user_id)
      .then(response => response.json())
      .then(data => {
            console.log(data);
            class_list = data;
            AddTable(data);
      })
}

// Event listeners for navigation buttons
document.getElementById("prevBtn").addEventListener("click", function() {
    previousPage(class_list);
});

document.getElementById("nextBtn").addEventListener("click", function() {
    nextPage(class_list);
});

// Event listener for delete button
document.getElementById("deleteBtn").addEventListener("click", function() {
    deleteSelected();
});

// Search the class
function executeSearch() {
    var searchBar = document.getElementById("searchBar");
    var searchBarVal = searchBar.value.toLowerCase();
    var filteredList = class_list.filter(function(c) {
        return c.title.toLowerCase().includes(searchBarVal) || c.id.toString().toLowerCase().includes(searchBarVal);
    });
    currentPage = 0; // Reset to the first page
    AddTable(filteredList);
    Countclass(filteredList);
}