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

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  window.location = "http://localhost:8080/fridge";
}

function onLoad() {
  gapi.load('auth2', function() {
    gapi.auth2.init();
  });
}

// welcome.html

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
  window.location = "http://localhost:8080";
}

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  window.location = "http://localhost:8080/fridge";
}

function onLoad() {
  gapi.load('auth2', function() {
    gapi.auth2.init();
  });
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
