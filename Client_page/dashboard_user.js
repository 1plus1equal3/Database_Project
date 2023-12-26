function createExamDiv(){
    
}

function loadQuestion(){
    fetch('http://localhost:5000/request_exam', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      })
      .then(response => response.json())
      .then(data => {
            console.log(data);
      })
}