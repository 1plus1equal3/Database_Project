var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

var currentPage = 0;
var itemPerPage = 7;

// Display the student's list
function AddTable(student_list) {
    var tableBody = document.getElementById("dataTableBody");
    tableBody.innerHTML = ''; // Clear existing rows

    student_list.forEach(function (student, index) {
        if (index >= itemPerPage * currentPage && index < itemPerPage * (currentPage + 1)) {
            var newRow = AddRow(index + 1, student.name, student.id, student.best_result, student.avg_result, student.num_of_tests);
            tableBody.appendChild(newRow);
        }
    });

    CountStudent(student_list);
}

function AddRow(no, name, id, best_result, avg_result, num_of_tests) {
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

    var best_result_cell = document.createElement("td");
    best_result_cell.textContent = best_result;
    row.appendChild(best_result_cell);

    var avg_result_cell = document.createElement("td");
    avg_result_cell.textContent = avg_result;
    row.appendChild(avg_result_cell);

    var num_of_tests_cell = document.createElement("td");
    num_of_tests_cell.textContent = num_of_tests;
    row.appendChild(num_of_tests_cell);

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

// Sample data for demonstration
const students_list = [
    { name: "Pham Quang Huy", id: "20215207", best_result: "10", avg_result: "10", num_of_tests: "5" },
    { name: "Tran Thuy Chau", id: "20215182", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Nguyen Dang Duy", id: "20210272", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Bui Duc Viet", id: "20215254", best_result: "10", avg_result: "7", num_of_tests: "10" },
    { name: "Hoang Van Khang", id: "20215182", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Chu Xuan Minh", id: "20235527", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Phan Ha Quyen", id: "20225224", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Nguyen Manh Cuong", id: "202151844", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Phan Dinh Trung", id: "20230093", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Nguyen Hoang Viet", id: "20220050", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Vu Thuong Tin", id: "20230091", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Nguyen Thuy Anh", id: "20215306", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Nguyen Cong Duy", id: "20215188", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Do Hong Hai", id: "20215199", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Tran Quang Hung", id: "20235502", best_result: "10", avg_result: "10", num_of_tests: "10" },
    { name: "Do Dang Vu", id: "20235578", best_result: "10", avg_result: "10", num_of_tests: "10" }
];

// Initial render
AddTable(students_list);

// Event listeners for navigation buttons
document.getElementById("prevBtn").addEventListener("click", function() {
    previousPage(students_list);
});

document.getElementById("nextBtn").addEventListener("click", function() {
    nextPage(students_list);
});

// Search the student
function executeSearch() {
    var searchBar = document.getElementById("searchBar");
    var searchBarVal = searchBar.value.toLowerCase();
    var searchOption = document.getElementsByName("searchOption");
    var searchOptionVal;
    if (searchOption[0].checked) {
        searchOptionVal = 0;
    } else {
        searchOptionVal = 1;
    }
    var filteredList = students_list.filter(function(student) {
        if (searchOptionVal === 0) {
            return student.name.toLowerCase().includes(searchBarVal);
        } else {
            return student.id.toLowerCase().includes(searchBarVal);
        }
    });
    currentPage = 0; // Reset to the first page
    AddTable(filteredList);
    CountStudent(filteredList);
}

function CountStudent(student_list) {
    var number_student = student_list.length;
    var student_num = document.getElementById("NumberOfStudent");
    student_num.textContent = number_student;
}