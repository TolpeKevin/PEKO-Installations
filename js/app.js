let customers;

const getDOMs = function() {
    customers = document.querySelectorAll('.customer')
    console.log(customers[1]['childNodes'][1])
}

const addListeners = function() {
    for(let customer of customers) {
        customer['childNodes'][1].addEventListener('click', function() {
            customer.classList.toggle('expand')
        })
    }
}

const init = function() {
    /* fetch('http://127.0.0.1:5000/')
    .then(response => response.json())
    .then(json => console.log(json))
    .catch(error => console.error(`Error: ${error}`)); */

    getDOMs()
    addListeners()

};
  
document.addEventListener('DOMContentLoaded', init);