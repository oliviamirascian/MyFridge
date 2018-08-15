// This function will hide the add button and show the text
// input that will allow the user to add an item to their
// food list

function addFood(){
  fetch("/fridgefood", {
    method: "POST",
    body: JSON.stringify({
      addFood: document.getElementById("addFoodText").value,
      expirationDate: document.getElementById("addFoodDate").value,
    })
  }).then((response) => response.json())
  .then(function(jsonfoodID) {
    console.log(jsonfoodID);
  })
}

function checkExpirationDate(){
  var today = new Date();
  if ((today.getMonth()+1) < 10){
    var month = "0" + String(today.getMonth()+1);
  } else {
    var month = String(today.getMonth()+1);
  }
  if (today.getDate() < 10){
    var day = "0"+ String(today.getDate());
  } else {
    var day = String(today.getDate());
  }
  // sets up today's date
  var date = String(today.getFullYear())+month+day;
  var dateCompare = Number(date);
  var foodList = document.getElementsByClassName("fridgefood-div");
  var expiringSoon = document.getElementById("expiringSoon");
  var expired = document.getElementById("expired");
  console.log(foodList);
  expiredStore = []
  expiringSoonStore = []
  for (var i = 0; i < foodList.length; i++){
    var food = foodList[i];
    console.log(i);
    // console.log(foodList);
    console.log(food);
    var name = food.getElementsByTagName("p")[0].innerHTML;
    var foodExpiration = food.getElementsByTagName("p")[1].innerHTML;
    if(foodExpiration == "Expires  "){
      food.getElementsByTagName("p")[1].innerHTML = "Does not expire";
    }
    else {
      var foodExpirationCompare = Number(foodExpiration.replace(/-|Expires| /g,""));
      if ((foodExpirationCompare - dateCompare) <= 0){
        // food.classList.add("expired-div");
        // expired.appendChild(food);
        expiredStore.push(food);
      }
      else if ((foodExpirationCompare - dateCompare) <= 7){
        // food.classList.add("expiringsoon-div");
        expiringSoonStore.push(food);
      }
    }
  }
  for (var i = 0; i < expiredStore.length; i++) {
    expired.appendChild(expiredStore[i]);
  }
  for (var i = 0; i < expiringSoonStore.length; i++) {
    expiringSoon.appendChild(expiringSoonStore[i]);
  }

}


document.addEventListener('DOMContentLoaded', () => {
  button = document.getElementById('addFoodButton');
  button.onclick = function() {
    const foodForm = document.getElementById('addFoodForm');
    if (foodForm.style.display === 'inline-block') {
      foodForm.style.display = 'none';
    } else {
      foodForm.style.display = 'inline-block';
    }
  }
});
