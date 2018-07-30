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

//welcome.html
function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log('User signed out.');
  });
}
