// This function will hide the add button and show the text
// input that will allow the user to add an item to their
// food list
function addToTextInput(){
  var addButton = document.getElementsByClassName('addButton');
  var textInput = document.getElementsByClassName('textAddFood');
  var addText = document.getElementsByClassName('addText');

  addButton.style.display = "none";
  textInput.style.display = "block";
}

// This function will hide the remove button and show the text
// input that will allow the user to remove an item from their
// food list
function removeToTextInput(){
  var removeButton = document.getElementsByClassName('removeButton');
  var textInput = document.getElementsByClassName('textRemoveFood');
  var removeText = document.getElementsByClassName('removeText');

  removeButton.style.display = "none";
  textInput.style.display = "block";
}

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

// This function will move an object from the Today list to the
// History list in the NutriTracker
function moveToHistory(){

}

function addItemToFridge(){
  var ul = document.getElementById("listFridge");
  var input = document.getElementById("addFoodFridge");
  var li = document.createElement('li');
  li.setAttribute('id',input.value);
  li.appendChild(document.createTextNode(input.value));
  ul.appendChild(li);
}

function removeItemFromFridge(){
  var ul = document.getElementById("listFridge");
  var input = document.getElementById("removeFoodFridge");
  var item = document.getElementById(input.value);
  ul.removeChild(item);
}

// welcome.html

// function signOut() {
//   var auth2 = gapi.auth2.getAuthInstance();
//   auth2.signOut().then(function () {
//   });
//   window.location = "http://localhost:8080";
// }

// welcome.html

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
