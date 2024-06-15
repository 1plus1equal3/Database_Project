var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

function AddStudent() {
    var student_id = document.getElementById("student_id");
    
    // Check if the student_id only have 1 id
    var student_id_list;
    if(student_id.value.split(",").length < 1 && student_id.value != "") {
        student_id_list = [student_id.value];
    }else{
        student_id_list = student_id.value.split(",");
    }

    // Process multiple student_ids
    var Ids = [];
    for (var i = 0; i < student_id_list.length; i++) {
        Ids.push(student_id_list[i]);
    }
    console.log({'student_ids': Ids});

    // Send a POST request to the server
    fetch("http://localhost:5000/add_student_to_class", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'student_ids': Ids, 'class_id': localStorage.getItem("class_id")}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.success) alert("Add student successfully!");
        else alert("Add student failed!");
    });
}