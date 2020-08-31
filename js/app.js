let page, customers;

const getDOMsByPage = function(page) {

    if(page == 'js-dashboard'){
    }
    else if(page == 'js-customers'){
        customers = document.querySelectorAll('.customer')
    }
    else if(page == 'js-maintenance'){
    }

    
}

const addListeners = function(page) {

    if(page == 'js-dashboard'){
    }
    else if(page == 'js-customers'){
        for(let customer of customers) {
            customer['childNodes'][1].addEventListener('click', function() {
                customer.classList.toggle('expand')
            })
        }
    }
    else if(page == 'js-maintenance'){
    }    
}

const getData = function() {
    if(page == 'js-dashboard'){
        
    }
    else if(page == 'js-customers'){
        fetch('http://127.0.0.1:5000/installaties')
        .then(response => response.json())
        .then(json => console.log(json))
        .catch(error => console.error(`Error: ${error}`));
    }
    else if(page == 'js-maintenance'){
    }
}

const init = function() {
    /* fetch('http://127.0.0.1:5000/')
    .then(response => response.json())
    .then(json => console.log(json))
    .catch(error => console.error(`Error: ${error}`)); */

    page = document.querySelector('body').classList.value

    getData()
    getDOMsByPage(page)
    addListeners(page)

};
  
document.addEventListener('DOMContentLoaded', init);