fetch('http://localhost:5000/getUserInfo?user_id=' + localStorage.getItem('user_id'), {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  .then(response => response.json())
  .then(data => {
        console.log(data);
        var user_info = document.getElementById("user_info");
        var user_previlege = "Administrator";
        if(data.user_type == 0) {
            user_previlege = "Student";
        }
        user_info.innerHTML = `
      <tr>
        <th>UserID</th>
        <td>${data.user_id}</td>
      </tr>
      <tr>
        <td>The UserID that identifies you on TestGen. You cannot change your UserID.</td>
      </tr>

      <tr>
        <th>Username</th>
        <td>${data.username}</td>
      </tr>
      <tr>
        <td>The name that is used for ID verification and that appears on your certificates.</td>
      </tr>
      
      <tr>
          <th>Email</th>
          <td>${data.email}</td>
      </tr>
      <tr>
          <td>You will receive messages from TestGen at this address</td>
      </tr>

      <tr>
          <th>User Type</th>
          <td>${user_previlege}</td>
      </tr>
      `;
      var username = localStorage.getItem("username");
      document.getElementById("username").textContent = username;
  })

