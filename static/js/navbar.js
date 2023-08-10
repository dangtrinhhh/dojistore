// navbar.js

const menuIcon = document.querySelector('.menu-icon');
const sidebar = document.querySelector('.sidebar');

menuIcon.addEventListener('click', () => {
    sidebar.style.width = sidebar.style.width === '250px' ? '0' : '250px';
});
