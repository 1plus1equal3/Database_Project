//Display random 10 students
function AddTable(student_list) {
    var tableBody = document.getElementById("dataTableBody");
    for (var i = 0; i < student_list.length && i < 5; i++) {
        var student = student_list[i];
        var newRow = AddRow(student.name, student.id, student.best_result, student.avg_result, student.num_of_tests, student.avg_time);
        tableBody.appendChild(newRow);
    }
}

function AddRow(name, id, best_result, avg_result, num_of_tests) {
    var row = document.createElement("tr");

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

students_list = [
    {
        name: "Pham Quang Huy",
        id: "20215207",
        best_result: "10",
        avg_result: "10",
        num_of_tests: "5",
    },
    {
        name: "Tran Thuy Chau",
        id: "20215182",
        best_result: "10",
        avg_result: "10",
        num_of_tests: "10",
    },
    {
        name: "Nguyen Dang Duy",
        id: "20210272",
        best_result: "10",
        avg_result: "10",
        num_of_tests: "10",
    },
    {
        name: "Bui Duc Viet",
        id: "20215254",
        best_result: "10",
        avg_result: "7",
        num_of_tests: "10",
    },
    {
        name: "Hoang Van Khang",
        id: "20215182",
        best_result: "10",
        avg_result: "10",
        num_of_tests: "10",
    }
]

AddTable(students_list)