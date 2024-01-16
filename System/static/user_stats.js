var username = localStorage.getItem("username");
document.getElementById("username").textContent = username;

function getUserID(){
    var url_string = window.location.href;
    var url = new URL(url_string);
    var user_id = url.searchParams.get("user_id");
    return user_id;
}

function getUserStats(){
    var user_id = getUserID();
    fetch("http://localhost:5000/statistic" + "?user_id=" + user_id)
      .then(response => response.json())
      .then(data => {
            console.log(data);
            // Create the first image element
            var firstImage = document.createElement("img");
            firstImage.src = 'statistic_barchart.png';
            firstImage.alt = "First Image";

            // Create the second image element
            var secondImage = document.createElement("img");
            secondImage.src = 'statistic_piechart.png';
            secondImage.alt = "Second Image";

            // Create div containers for images
            var firstImageContainer = document.createElement("div");
            firstImageContainer.className = "image-container"
            firstImageContainer.appendChild(firstImage);
            firstImageContainer.style.marginBottom = "20px";

            var secondImageContainer = document.createElement("div");
            secondImageContainer.className = "image-container"
            secondImageContainer.appendChild(secondImage);
            secondImageContainer.style.marginBottom = "5px";

            var statistic = document.createElement("div");
            statistic.className = "row";
            var maxValue = document.createElement("div");
            maxValue.className = "col";
            maxValue.textContent = "Max Score: " + data.max;
            var minValue = document.createElement("div");
            minValue.className = "col";
            minValue.textContent = "Min Score: " + data.min;
            var avgValue = document.createElement("div");
            avgValue.className = "col";
            avgValue.textContent = "Avg Score: " + data.average;
            statistic.appendChild(maxValue);
            statistic.appendChild(minValue);
            statistic.appendChild(avgValue);

            // Get the content div and append image containers
            var chart = document.getElementById("chart");
            chart.appendChild(firstImageContainer);
            chart.appendChild(secondImageContainer);
            var stat = document.getElementById("stats");
            stat.appendChild(statistic);
      })
}