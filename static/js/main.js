// const loggings = document.querySelector('.buy-tickets')
const buyBtns = document.querySelectorAll('.js-buy-ticket')
const closeBtn = document.querySelector('.modal-close')
const modalContainer = document.querySelector('.js-modal-container')
const closeBtn2 = document.querySelector('.modal-close2')
const modalContainer2 = document.querySelector('.js-modal-container2')
const modal = document.querySelector('.js-modal')
const modal2 = document.querySelector('#modal2')
const loginBtn = document.querySelector('.btn-login')
const registerBtn = document.querySelector('.btn-register')

loginBtn.addEventListener('click', () => {
    modal.classList.add("open")
    modal.classList.add("animated")
    modal.classList.add("FadeIn")
})

registerBtn.addEventListener('click', () => {
    modal2.classList.add("open")
    modal2.classList.add("animated")
    modal2.classList.add("FadeIn")
})

for (const buyBtn of buyBtns) {
    buyBtn.addEventListener('click', showBuyTickets)
}


function hideBuyTickets() {
    modal.classList.remove("open")
}

function hideBuyTickets2() {
    modal2.classList.remove("open")
}

// loggings.addEventListener('click', hideBuyTickets)

closeBtn.addEventListener('click', hideBuyTickets)
closeBtn2.addEventListener('click', hideBuyTickets2)

modal.addEventListener('click', hideBuyTickets)

modal2.addEventListener('click', hideBuyTickets)

modalContainer.addEventListener('click', function(event) {
    event.stopPropagation()
})

modalContainer2.addEventListener('click', function(event) {
    event.stopPropagation()
})