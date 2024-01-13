var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

function createTest(testInfo) {
    fetch('http://localhost:5000/create_test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(testInfo)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Redirect to the test page
            window.location.href = "http://localhost:5000/test_view.html?id=" + data.test_id;
        }else{
            alert(data.message);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function receiveTestInfo() {
    // Fetch values from the form
    var title = document.getElementById('title').value;
    var numQuestions = document.getElementById('numQuestions').value;
    var subject = document.getElementById('subject').value;
    var difficulty = document.getElementById('difficulty').value;
    var admin_id = localStorage.getItem("user_id");
    // Validate number of questions
    if (numQuestions <= 0 || isNaN(numQuestions)) {
        alert('Please enter a valid positive number of questions.');
        return;
    }

    // Perform any additional logic or validation if needed

    // Log the values (you can replace this with your logic to create the test)
    console.log('Title of the Test:', title);
    console.log('Number of Questions:', numQuestions);
    console.log('Subject of the Test:', subject);
    console.log('Difficulty Level:', difficulty);
    console.log('Admin ID:', admin_id);

    testInfo = {
        title: title,
        numQuestions: numQuestions,
        subject: subject,
        difficulty: difficulty,
        admin_id: admin_id
    }
    createTest(testInfo);
}