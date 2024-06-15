function DeleteClass() {
    var class_name = document.getElementById("class_name");
    var class_id = document.getElementById("class_id");
    
    // Check if the class_id only have 1 id
    var class_id_list;
    if(class_id.value.split(",").length < 1 && class_id.value != "") {
        class_id_list = [class_id.value];
    }else{
        class_id_list = class_id.value.split(",");
    }

    // Process multiple class_ids
    var Ids = [];
    for (var i = 0; i < class_id_list.length; i++) {
        Ids.push(class_id_list[i]);
    }
    console.log({'class_ids': Ids});
    // Send a DELETE request to the server
    fetch("http://localhost:5000/delete_class", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({'class_ids': Ids}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if(data.success) alert("Delete class successfully!");
        else alert("Delete class failed!");
    });
}