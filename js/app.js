let page, customers, extra, installationsform, nmbInst = 1, overlay;

const getDOMsByPage = function(page) {

    if(page == 'js-dashboard'){
    }
    else if(page == 'js-customers'){
        customers = document.querySelectorAll('.customer');
        overlay = document.querySelector('.js-overlay');
    }
    else if(page == 'js-new-customer'){
        extra = document.querySelector('.js-extra');
        installationsform = document.querySelector('.js-installations');
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

            console.log(customer['children'][0]['children'][0]['children'][1])

            customer['children'][0]['children'][0]['children'][1].addEventListener('click', function(){
                overlay.classList.toggle('show')
            })

            overlay['children'][0]['children'][0]['children'][2]['children'][1].addEventListener('click', function() {
                overlay.classList.remove('show')
            })

            customer['children'][2]['children'][1]['children'][0]['children'][1].addEventListener('click', function() {
                let id = customer['dataset']['id']
                let name = customer['dataset']['name']

                document.location.href = `/nieuweinstallatie.html?id=${id}&name=${name}`;
            })

            customer['children'][2]['children'][1]['children'][0]['children'][2].addEventListener('click', function() {
                let id = customer['dataset']['id']
                let name = customer['dataset']['name']

                document.location.href = `/updateinstallatie.html?id=${id}&name=${name}`;
            })

            customer['children'][2]['children'][0]['children'][0]['children'][1].addEventListener('click', function() {
                let id = customer['dataset']['id']
                let name = customer['dataset']['name']

                document.location.href = `/updatebedrijfsinfo.html?id=${id}&name=${name}`;
            })
        }
    }
    else if(page == 'js-new-customer'){
        extra.addEventListener('click', function(){
            nmbInst++

            installationsform.innerHTML += `<div class="u-mb-xxl flex flex_gutter installations">
            <p class="installations_label u-mb-clear">Installatie ${nmbInst}</p>

            <div class="flex_item u-mb u-1-of-2-bp3 u-3-of-4-bp4">
                <label for="adres-${nmbInst}" class="u-mb-sm">Adres</label>
                <input id="adres-${nmbInst}" class="custom_input" type="text">
            </div>
            <div class="flex_item u-mb u-1-of-2-bp3 u-1-of-4-bp4">
                <label for="type-${nmbInst}" class="u-mb-sm">Type</label>
                <input id="type-${nmbInst}" class="custom_input" type="text">
            </div>
            <div class="flex_item u-mb u-1-of-2-bp3 u-1-of-3-bp4">
                <label for="pnumber-${nmbInst}" class="u-mb-sm">P nummer</label>
                <input id="pnumber-${nmbInst}" class="custom_input" type="text">
            </div>
            <div class="flex_item u-mb u-1-of-2-bp3 u-1-of-3-bp4">
                <label for="installationdate-${nmbInst}" class="u-mb-sm">Installatiedatum</label>
                <input id="installationdate-${nmbInst}" class="custom_input" type="date">
            </div>
            <div class="flex_item u-mb u-1-of-2-bp3 u-1-of-3-bp4">
                <label for="reminder-${nmbInst}" class="u-mb-sm">Reminder (dagen)</label>
                <input id="reminder-${nmbInst}" class="custom_input" type="number">
            </div>
        </div>`
        })
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
    else if(page == 'js-new-customer'){
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