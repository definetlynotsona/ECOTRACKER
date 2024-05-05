// get the login button and container elements
const loginButton = document.getElementById('login');
const container = document.getElementById('container');

// add event listener to login button
loginButton.addEventListener('click', () => {
  // add fadeout class to container element
  container.classList.add('fadeout');
});

