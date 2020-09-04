let page, customers, overlay;

/* Customers */
let allCustomers;

/* New Customer */
let extra, installationsform, nmbInst = 1;

const getDOMsByPage = function(page) {

    if(page == 'js-dashboard'){
    }
    else if(page == 'js-customers'){
        
    }
    else if(page == 'js-new-customer'){
        installationsform = document.querySelector('.js-installations');
        extra = document.querySelector('.js-extra');
    }    
}



const addListeners = function(page) {

    if(page == 'js-dashboard'){
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

const createNewCustomer = function(name, phone, mail) {

    let body = JSON.stringify({"name": name.value, "phone": phone.value, "mail": mail.value})

    handleData(`http://127.0.0.1:5000/customers`, successfull, 'POST', body)

    return false
}

const successfull = function(json) {

}

const showCustomers = function(json) {

    allCustomers = document.querySelector('.js-content');
    let html = '';

    for(j of json){

        html += `<div class="card customer" data-id="${j['id']}" data-name="${j['name']}">
                    <div class="flex customer_sm">
                        <div class="flex customer_edit">
                            <p class="u-mb-clear">${j['name']}</p>
                            <svg class="icon icon_edit" aria-hidden="true" focusable="false" class="svg-inline--fa fa-trash fa-w-14" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M432 32H312l-9.4-18.7A24 24 0 0 0 281.1 0H166.8a23.72 23.72 0 0 0-21.4 13.3L136 32H16A16 16 0 0 0 0 48v32a16 16 0 0 0 16 16h416a16 16 0 0 0 16-16V48a16 16 0 0 0-16-16zM53.2 467a48 48 0 0 0 47.9 45h245.8a48 48 0 0 0 47.9-45L416 128H32z"></path></svg>
                        </div>
                        
                        <svg class="icon customer_arrow" aria-hidden="true" focusable="false" class="svg-inline--fa fa-angle-down fa-w-10" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path fill="currentColor" d="M143 352.3L7 216.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.2 9.4-24.4 9.4-33.8 0z"></path></svg>
                    </div>
                    <hr />
                    <div class="customer_lg">
                        <div class="customer_info">
                            <div class="flex customer_edit">
                                <p class="u-mb customer_subtitle">Bedrijfsinformatie</p>
                                <svg class="icon u-mb" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="pen" class="svg-inline--fa fa-pen fa-w-16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M290.74 93.24l128.02 128.02-277.99 277.99-114.14 12.6C11.35 513.54-1.56 500.62.14 485.34l12.7-114.22 277.9-277.88zm207.2-19.06l-60.11-60.11c-18.75-18.75-49.16-18.75-67.91 0l-56.55 56.55 128.02 128.02 56.55-56.55c18.75-18.76 18.75-49.16 0-67.91z"></path></svg>
                            </div>
                            

                            <div class="flex u-mb-md">
                                <div class="flex flex_item u-mb-clear u-1-of-2-bp3 u-1-of-3-bp4">
                                    <p class="u-mr-md u-mb-clear"><b>Tel.:</b></p>
                                    <p class="u-mr-md u-mb-clear">${j['phone']}</p>
                                </div>

                                <div class="flex flex_item u-mb-clear u-1-of-2-bp3 u-1-of-3-bp4">
                                    <p class="u-mr-md u-mb-clear"><b>E-mail:</b></p>
                                    <p class="u-mr-md u-mb-clear">${j['mail']}</p>
                                </div>
                            </div>
                            <div class="flex u-mb-xxl">
                                <div class="flex flex_item u-mb-clear u-1-of-2-bp3 u-1-of-3-bp4">
                                    <p class="u-mr-md u-mb-clear"><b>Aantal installaties:</b></p>
                                    <p class="u-mr-md u-mb-clear"></p>
                                </div>
                            </div>
                        </div>

                        <div class="customer_info">
                            <div class="flex customer_edit">
                                <p class="u-mb customer_subtitle">Installaties</p>
                                <svg class="icon u-mb" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="plus" class="svg-inline--fa fa-plus fa-w-14" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M416 208H272V64c0-17.67-14.33-32-32-32h-32c-17.67 0-32 14.33-32 32v144H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h144v144c0 17.67 14.33 32 32 32h32c17.67 0 32-14.33 32-32V304h144c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z"></path></svg>
                                <svg class="icon u-mb" aria-hidden="true" focusable="false" data-prefix="fas" data-icon="pen" class="svg-inline--fa fa-pen fa-w-16" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M290.74 93.24l128.02 128.02-277.99 277.99-114.14 12.6C11.35 513.54-1.56 500.62.14 485.34l12.7-114.22 277.9-277.88zm207.2-19.06l-60.11-60.11c-18.75-18.75-49.16-18.75-67.91 0l-56.55 56.55 128.02 128.02 56.55-56.55c18.75-18.76 18.75-49.16 0-67.91z"></path></svg>
                            </div>
                        </div>
                    </div>
                </div>`
    }

    allCustomers.innerHTML += html

    customers = document.querySelectorAll('.customer');
    overlay = document.querySelector('.js-overlay');

    listenersCustomer()

    handleData(`http://127.0.0.1:5000/installations`, addInstallations)

}

const listenersCustomer = function() {
    for(let customer of customers) {

        /* Expand the customer container */

        customer['children'][0].addEventListener('click', function() {
            customer.classList.toggle('expand')
        })

        /* Show overlay by pressing the trashcan */

        customer['children'][0]['children'][0]['children'][1].addEventListener('click', function(){
            overlay.classList.toggle('show')
        })

        /* Hide overlay by pressing cancel */

        overlay['children'][0]['children'][0]['children'][2]['children'][1].addEventListener('click', function() {
            overlay.classList.remove('show')
        })

        /* Navigate to New Installation */

        customer['children'][2]['children'][1]['children'][0]['children'][1].addEventListener('click', function() {
            let id = customer['dataset']['id']
            let name = customer['dataset']['name']

            document.location.href = `/nieuweinstallatie.html?id=${id}&name=${name}`;
        })

        /* Navigate to Update Installation */

        customer['children'][2]['children'][1]['children'][0]['children'][2].addEventListener('click', function() {
            let id = customer['dataset']['id']

            document.location.href = `/updateinstallatie.html`;
        })

        /* Navigate to Update Companyinfo */

        customer['children'][2]['children'][0]['children'][0]['children'][1].addEventListener('click', function() {
            let id = customer['dataset']['id'];

            document.location.href = `/updatebedrijfsinfo.html?id=${id}`;
        })
    }
}

const editCompany = function(json) {
    let edit = document.querySelector('.js-form')

    edit['children'][1]['children'][0]['children'][1].value = json[0]['name']

    edit['children'][2]['children'][0]['children'][1].value = json[0]['phone']

    edit['children'][2]['children'][1]['children'][1].value = json[0]['mail']
}

const updateCompany = function(name, phone, mail) {

    let body = JSON.stringify({"name": name.value, "phone": phone.value, "mail": mail.value})

    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');


    handleData(`http://127.0.0.1:5000/customers/${id}`, successfull, 'PUT', body)
    return false

}

const addInstallations = function(json) {

    for(j of json) {
        for(c of customers){
            if(j["id"] == c["dataset"]["id"]){

                /* Add the amount of installations to the card */

                console.log(j['installations'].length)

                for(i of j['installations']){

                    let html = `<div class="u-mb flex installations">
                                <div class="flex_item u-3-of-4-bp4">
                                    <div class="flex">
                                        <p class="u-mb-md u-mr-md"><b>Adres:</b></p>
                                        <p class="u-mb-md">${i['adres']}</p>
                                    </div>
                                </div>
                                <div class="flex_item u-1-of-2-bp3 u-1-of-4-bp4">
                                    <div class="flex">
                                        <p class="u-mb-md u-mr-md"><b>Type:</b></p>
                                        <p class="u-mb-md">${i['type']}</p>
                                    </div>
                                </div>
                                <div class="flex_item u-1-of-2-bp3 u-1-of-3-bp4">
                                    <div class="flex">
                                        <p class="u-mb-md u-mr-md"><b>P nummer:</b></p>
                                        <p class="u-mb-md">${i['p_nummer']}</p>
                                    </div>
                                </div>
                                <div class="flex_item u-1-of-2-bp3 u-1-of-3-bp4">
                                    <div class="flex">
                                        <p class="u-mb-md u-mr-md"><b>Datum installatie:</b></p>
                                        <p class="u-mb-md">${toDate(i['datum_installatie'])}</p>
                                    </div>
                                </div>
                                <div class="flex_item u-1-of-2-bp3 u-1-of-3-bp4">
                                    <div class="flex">
                                        <p class="u-mb-md u-mr-md"><b>Laatste onderhoud:</b></p>
                                        <p class="u-mb-md">${toDate(i['laatste_onderhoud'])}</p>
                                    </div>
                                </div>
                                <div class="flex_item u-1-of-2-bp3 u-1-of-3-bp4">
                                    
                                    <div class="flex">
                                        <p class="u-mb-md u-mr-md"><b>Reminder:</b></p>
                                        <p class="u-mb-md">na ${i['reminder']} dagen</p>
                                    </div>
                                </div>
                            </div>`
                    
                    c['children'][2]['children'][1].innerHTML += html
                }
            }
        }
    }
}

const getData = function() {
    if(page == 'js-dashboard'){
        
    }
    else if(page == 'js-customers'){
        handleData(`http://127.0.0.1:5000/customers`, showCustomers)
    }
    else if(page == 'js-new-customer'){
    }
    else if(page == 'js-update-customer'){

        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');

        handleData(`http://127.0.0.1:5000/customers/${id}`, editCompany);
    }
}

const handleData = function(url, callback, method = 'GET', body = null) {
    fetch(url, {
      method: method,
      body: body,
      headers: { 'content-type': 'application/json', 'Access-Control-Allow-Headers': '*' }
    })
      .then(function(response) {
        if (!response.ok) {
          throw Error(`${response.statusText}. Status Code: ${response.status}`);
        } else {
          return response.json();
        }
      })
      .then(function(jsonObject) {
        callback(jsonObject);
      })
      .catch(function(error) {
        console.error(`Error: ${error}`);
      });
  };

const toDate = function(seconds) {
    let date = new Date(0);
    date.setUTCSeconds(seconds)

    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();

    return `${day}/${month}/${year}`
}

const init = function() {

    page = document.querySelector('body').classList.value

    getData()
    getDOMsByPage(page)
    addListeners(page)

};
  
document.addEventListener('DOMContentLoaded', init);