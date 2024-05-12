function DeleteStudent() {
    var student_name = document.getElementById("student_name");
    var student_id = document.getElementById("student_id");
    
    var classItem = {
        name: student_name.value,
        id: student_id.value, 
    }
    console.log(classItem);
    student_name.value = "";
    student_id.value = "";
}