const init = function() {
    fetch('http://127.0.0.1:5000/')
    .then(response => response.json())
    .then(json => console.log(json))
    .catch(error => console.error(`Error: ${error}`));
};
  
document.addEventListener('DOMContentLoaded', init);