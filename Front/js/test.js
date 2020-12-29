function logSubmit(event) {
    console.log(event)
    log.textContent = `Form Submitted! Time stamp: ${event.timeStamp}`;
    event.preventDefault();
  }

const init = function() {
    const form = document.getElementById('form');
    const log = document.getElementById('log');
    form.addEventListener('submit', logSubmit);
}
  

  document.addEventListener('DOMContentLoaded', init);