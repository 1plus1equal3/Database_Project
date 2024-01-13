function submitForm() {
    // Get form values
    var username = document.getElementById("exampleFirstName").value;
    var email = document.getElementById("exampleInputEmail").value;
    //var userId = document.getElementById("exampleUserID").value;
    var password = document.getElementById("exampleInputPassword").value;
    var repeatPassword = document.getElementById("exampleRepeatPassword").value;

    if((username == null || username == "")
    &&(email == null || email == "")
    //&&(userId == null || userId == "")
    &&(password == null || password == "")
    &&(repeatPassword == null || repeatPassword == "")){
        alert('Please enter all register information');
        return;
    }else{
    // Check if password and repeat password match
    if (password !== repeatPassword) {
        alert("Password and Repeat Password do not match. Please try again.");
        document.getElementById("exampleInputPassword").value = "";
        document.getElementById("exampleRepeatPassword").value = "";
        return;
    }

    // Create JSON object
    var userObject = {
        username: username,
        email: email,
        //user_id: userId,
        password: password,
        user_type: 0
    };

    fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(userObject),
          })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              alert('Register successful');
              // Redirect to the login page after successful registration
              window.location.href = "http://localhost:5000/";
            } else {
              alert('Register failed');
            }
          })
          .catch((error) => {
            console.error('Error:', error);
          });
}
}
