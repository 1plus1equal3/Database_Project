function submitForm(event) {
  event.preventDefault();
  // Get the entered username and password
  var username = document.getElementById('exampleInputEmail').value;
  var password = document.getElementById('exampleInputPassword').value;

  // Check if username or password fields are empty
  if (username.trim() === '' || password.trim() === '') {
      alert('Please enter both username and password');
  } else {
      // Create a JSON object with the entered data
      var loginData = {
          username: username,
          password: password
          // You can add more data if needed
      };

      fetch('http://localhost:5000/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(loginData),
      })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  alert('Login successful');
                  user_id = data.user_id;

                  // Save user_id in localStorage
                  localStorage.setItem('user_id', user_id);
                  var newUrl = "dashboard_user.html";
                  window.location = newUrl;
              } else {
                  alert('Login failed');
              }
          })
          .catch((error) => {
              console.error('Error:', error);
          });
  }
}

// Function to retrieve user_id from the cookie
function getUserIdFromCookie() {
  var name = 'user_id=';
  var decodedCookie = decodeURIComponent(document.cookie);
  var cookieArray = decodedCookie.split(';');
  for (var i = 0; i < cookieArray.length; i++) {
      var cookie = cookieArray[i].trim();
      if (cookie.indexOf(name) === 0) {
          return cookie.substring(name.length, cookie.length);
      }
  }
  return null;
}

function getUserIdFromLocalStorage(){
    return localStorage.getItem('user_id');
}
