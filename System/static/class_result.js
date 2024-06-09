var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

var currentPage = 0;
var itemsPerPage = 7;
var current_student_list;
var current_type;
// Display the student's list

function SingleOrDual() {
    var studentNameBar = document.getElementById("searchBarStudentName");
    var studentName = studentNameBar.value;
    var testIDBar = document.getElementById("searchBarTestID");
    var testID = testIDBar.value;
    if(studentName === "" && testID === "") {
        DualSearch();
    } else {
        SingleSearch();
    }
}

function SingleSearch() {
    var student_list = loadData();
    current_student_list = loadData();
    current_type = 1;
    AddTable(student_list, 1);
    console.log("Single");
    console.log(current_student_list);
}

function DualSearch() {
    var student_list = loadData2();
    current_student_list = loadData2();
    current_type = 2;
    AddTable(student_list, 2);
    console.log("Dual");
    console.log(current_student_list);
}

function AddTable(student_list, type) {
    var tableBody = document.getElementById("dataTableBody");
    tableBody.innerHTML = ''; // Clear existing rows
    var tableHead = document.getElementById("dataTableHead");
    tableHead.innerHTML = ''; // Clear existing table head
    console.log(type);
    if(type === 1) {
        tableHead.innerHTML = `<tr>
                <th>No</th>
                <th>Student's name</th>
                <th>Student's ID</th>
                <th>Test's ID</th>
                <th>Result</th>
            </tr>`;
    } else if(type === 2) {
        tableHead.innerHTML = `<tr>
                <th>No</th>
                <th>Student's name</th>
                <th>Student's ID</th>
                <th>Best result</th>
                <th>Average result</th>
            </tr>`;
    }
    student_list.forEach(function (student, index) {
        if (index >= itemsPerPage * currentPage && index < itemsPerPage * (currentPage + 1)) {
            var newRow;
            if(type === 1) {
                newRow = AddRow1(index + 1, student.name, student.sid, student.tid, student.result);
            } else if(type === 2) {
                newRow = AddRow2(index + 1, student.name, student.sid, student.best_result, student.avg_result);
            }
            tableBody.appendChild(newRow);
        }
    });
}

function AddRow1(no, name, sid, tid, result) {
    var row = document.createElement("tr");

    var no_cell = document.createElement("td");
    no_cell.textContent = no;
    row.appendChild(no_cell);

    var name_cell = document.createElement("td");
    name_cell.textContent = name;
    row.appendChild(name_cell);

    var id_cell = document.createElement("td");
    id_cell.textContent = sid;
    row.appendChild(id_cell);

    var tid_cell = document.createElement("td");
    tid_cell.textContent = tid;
    row.appendChild(tid_cell);

    var result_cell = document.createElement("td");
    result_cell.textContent = result;
    row.appendChild(result_cell);
    
    return row;
}

function AddRow2(no, name, sid, best_result, avg_result) {
    var row = document.createElement("tr");

    var no_cell = document.createElement("td");
    no_cell.textContent = no;
    row.appendChild(no_cell);

    var name_cell = document.createElement("td");
    name_cell.textContent = name;
    row.appendChild(name_cell);

    var id_cell = document.createElement("td");
    id_cell.textContent = sid;
    row.appendChild(id_cell);

    var best_result_cell = document.createElement("td");
    best_result_cell.textContent = best_result;
    row.appendChild(best_result_cell);

    var avg_result_cell = document.createElement("td");
    avg_result_cell.textContent = avg_result;
    row.appendChild(avg_result_cell);
    
    return row;
}


function getPageCount(student_list) {
    if (!student_list || student_list.length === 0) {
        return 0;
    }
    return Math.ceil(student_list.length / itemsPerPage);
}

function previousPage(current_student_list) {
    if (currentPage > 0) {
        currentPage--;
        AddTable(current_student_list, current_type);
        console.log(currentPage);
    } else {
        console.log("You are on the first page");
    }
}

function nextPage(current_student_list) {
    var totalPages = getPageCount(current_student_list);
    console.log("Next page button pressed");
    console.log("Total page:", totalPages);
    console.log("Current page:", currentPage);
    if (totalPages < 0) {
        console.log("No items in the student list");
        return;
    }
    if (currentPage < totalPages - 1) {
        currentPage++;
        AddTable(current_student_list, current_type);
        console.log(currentPage);
    } else {
        console.log("You are on the last page");
    }
}

function firstPage(current_student_list) {
    if (currentPage !== 0) {
        currentPage = 0;
        AddTable(current_student_list, current_type);
        console.log("Navigated to first page");
    }
}

function lastPage(current_student_list) {
    var totalPages = getPageCount(current_student_list);
    if (currentPage !== totalPages - 1) {
        currentPage = totalPages - 1;
        AddTable(current_student_list, current_type);
        console.log("Navigated to last page");
    }
}

function loadData() {
    // Sample data for demonstration
    const students_list = [
        { name: "Pham Quang Huy", sid: "20215207", tid: "10", result: "10" },
        { name: "Tran Thuy Chau", sid: "20215182", tid: "10", result: "10" },
        { name: "Nguyen Dang Duy", sid: "20210272", tid: "10", result: "10" },
        { name: "Bui Duc Viet", sid: "20215254", tid: "10", result: "10" },
        { name: "Hoang Van Khang", sid: "20215182", tid: "10", result: "10" },
        { name: "Chu Xuan Minh", sid: "20235527", tid: "10", result: "10" },
        { name: "Phan Ha Quyen", sid: "20225224", tid: "10", result: "10" },
        { name: "Nguyen Manh Cuong", sid: "202151844", tid: "10", result: "10" },
        { name: "Phan Dinh Trung", sid: "20230093", tid: "10", result: "10" },
        { name: "Nguyen Hoang Viet", sid: "20220050", tid: "10", result: "10" },
        { name: "Vu Thuong Tin", sid: "20230091", tid: "10", result: "10" },
        { name: "Nguyen Thuy Anh", sid: "20215306", tid: "10", result: "10" },
        { name: "Nguyen Cong Duy", sid: "20215188", tid: "10", result: "10" },
        { name: "Do Hong Hai", sid: "20215199", tid: "10", result: "10" },
        { name: "Tran Quang Hung", sid: "20235502", tid: "10", result: "10" },
        { name: "Do Dang Vu", sid: "20235578", tid: "10", result: "10" }
    ];
    return students_list; 
}

function loadData2() {
    const students_list = [
        { name: "Pham Quang Huy", sid: "20215207", best_result: "10", avg_result: "10" },
        { name: "Tran Thuy Chau", sid: "20215182", best_result: "10", avg_result: "10" },
        { name: "Nguyen Dang Duy", sid: "20210272", best_result: "10", avg_result: "10" },
        { name: "Bui Duc Viet", sid: "20215254", best_result: "10", avg_result: "10" },
        { name: "Hoang Van Khang", sid: "20215182", best_result: "10", avg_result: "10" },
        { name: "Chu Xuan Minh", sid: "20235527", best_result: "10", avg_result: "10" },
        { name: "Phan Ha Quyen", sid: "20225224", best_result: "10", avg_result: "10" },
        { name: "Nguyen Manh Cuong", sid: "202151844", best_result: "10", avg_result: "10" },
        { name: "Phan Dinh Trung", sid: "20230093", best_result: "10", avg_result: "10" },
        { name: "Nguyen Hoang Viet", sid: "20220050", best_result: "10", avg_result: "10" },
        { name: "Vu Thuong Tin", sid: "20230091", best_result: "10", avg_result: "10" },
        { name: "Nguyen Thuy Anh", sid: "20215306", best_result: "10", avg_result: "10" },
        { name: "Nguyen Cong Duy", sid: "20215188", best_result: "10", avg_result: "10" },
        { name: "Do Hong Hai", sid: "20215199", best_result: "10", avg_result: "10" },
        { name: "Tran Quang Hung", sid: "20235502", best_result: "10", avg_result: "10" },
        { name: "Do Dang Vu", sid: "20235578", best_result: "10", avg_result: "10" }
    ];
    return students_list;
}

// Initial render
AddTable(loadData2(), 2);
current_student_list = loadData2();
current_type = 2;

// Event listeners for navigation buttons
document.getElementById("prevBtn").addEventListener("click", function() {
    previousPage(current_student_list); // Just pass the function name without parentheses
});

document.getElementById("nextBtn").addEventListener("click", function() {
    nextPage(current_student_list); // Just pass the function name without parentheses
});
document.getElementById("firstBtn").addEventListener("click", function() {
    firstPage(current_student_list);
});

document.getElementById("lastBtn").addEventListener("click", function() {
    lastPage(current_student_list);
});

