function DeleteClass() {
    var class_name = document.getElementById("class_name");
    var class_id = document.getElementById("class_id");
    
    var classItem = {
        name: class_name.value,
        id: class_id.value, 
    }
    console.log(classItem);

    class_name.value = "";
    class_id.value = "";
}