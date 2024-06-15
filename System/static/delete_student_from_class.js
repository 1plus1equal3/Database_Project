var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

var currentPage = 0;
var itemPerPage = 7;
var selectedStudents = [];
var students_list = [];

init();

// Display the student's list
function AddTable(student_list) {
    var tableBody = document.getElementById("dataTableBody");
    tableBody.innerHTML = ''; // Clear existing rows

    student_list.forEach(function (student, index) {
        if (index >= itemPerPage * currentPage && index < itemPerPage * (currentPage + 1)) {
            var newRow = AddRow(index + 1, student.username, student.user_id);
            tableBody.appendChild(newRow);
        }
    });
}

// function AddRow(no, name, id) {
//     var row = document.createElement("tr");

//     var no_cell = document.createElement("td");
//     no_cell.textContent = no;
//     row.appendChild(no_cell);

//     var name_cell = document.createElement("td");
//     name_cell.textContent = name;
//     row.appendChild(name_cell);

//     var id_cell = document.createElement("td");
//     id_cell.textContent = id;
//     row.appendChild(id_cell);

//     var delete_cell = document.createElement("td");
//     var delete_checkbox = document.createElement("input");
//     delete_checkbox.type = "checkbox";
//     delete_checkbox.value = id; // Set value as student ID for identification
//     delete_checkbox.addEventListener("change", function() {
//         if (this.checked) {
//             selectedStudents.push(this.value); // Add ID to selectedStudents array
//         } else {
//             var index = selectedStudents.indexOf(this.value);
//             if (index !== -1) {
//                 selectedStudents.splice(index, 1); // Remove ID from selectedStudents array
//             }
//         }
//     });
//     delete_cell.appendChild(delete_checkbox);
//     row.appendChild(delete_cell);

//     return row;
// }

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
    // Check if the ID is already in the selectedStudents array and set the checkbox state accordingly
    console.log(selectedStudents);
    if (selectedStudents.includes(id.toString())) {
        delete_checkbox.checked = true;
    } else {
        delete_checkbox.checked = false;
    }
    // Set value as class ID for identification
    delete_checkbox.value = id; 

    // Add an event listener for the change event
    delete_checkbox.addEventListener("change", function() {
        if (delete_checkbox.checked) {
            // If the checkbox is checked, add the ID to the selectedStudents array
            selectedStudents.push(delete_checkbox.value);
            console.log(selectedStudents);
        } else {
            // If the checkbox is unchecked, remove the ID from the selectedStudents array
            const index = selectedStudents.indexOf(delete_checkbox.value);
            selectedStudents.splice(index, 1);
            console.log(selectedStudents);
        }
    });

    delete_cell.appendChild(delete_checkbox);
    row.appendChild(delete_cell);

    return row;
}

function getPageCount(student_list) {
    if (!student_list || student_list.length === 0) {
        return 0;
    }
    return Math.ceil(student_list.length / itemPerPage);
}

function previousPage(student_list) {
    if (currentPage > 0) {
        currentPage--;
        AddTable(student_list);
        console.log(currentPage);
    } else {
        console.log("You are on the first page");
    }
}

function nextPage(student_list) {
    var totalPages = getPageCount(student_list);
    console.log("Next page button pressed");
    console.log("Total page:", totalPages);
    console.log("Current page:", currentPage);
    if (totalPages < 0) {
        console.log("No items in the student list");
        return;
    }
    if (currentPage < totalPages - 1) {
        currentPage++;
        AddTable(student_list);
        console.log(currentPage);
    } else {
        console.log("You are on the last page");
    }
}

// Delete selected students
function deleteSelected() {
    console.log("Delete selected Students:", selectedStudents);
    fetch('http://localhost:5000/delete_student_from_class', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'student_ids': selectedStudents, 'class_id': localStorage.getItem('class_id')})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.success) {
            alert("Delete student successfully!");
            init();
        } else {
            alert("Delete student failed!");
        }
    });
}

// Sample data for demonstration
// const students_list = [
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
function init() {
    // Fetch student list from the server
    fetch('http://localhost:5000/get_class_info?'+'c_id=' + localStorage.getItem('class_id') , {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        students_list = data.students;
        console.log(data);
        AddTable(students_list);
    });
}

// Event listeners for navigation buttons
document.getElementById("prevBtn").addEventListener("click", function() {
    previousPage(students_list);
});

document.getElementById("nextBtn").addEventListener("click", function() {
    nextPage(students_list);
});

// Event listener for delete button
document.getElementById("deleteBtn").addEventListener("click", function() {
    deleteSelected();
});

// Search the student
function executeSearch() {
    var searchBar = document.getElementById("searchBar");
    var searchBarVal = searchBar.value.toLowerCase();
    var filteredList = students_list.filter(function(student) {
        return student.username.toLowerCase().includes(searchBarVal) || student.user_id.toString().includes(searchBarVal);
    });
    currentPage = 0; // Reset to the first page
    AddTable(filteredList);
    CountStudent(filteredList);
}