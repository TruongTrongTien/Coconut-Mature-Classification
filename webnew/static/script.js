const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

if (registerLink) {
    registerLink.addEventListener('click', () => {
        wrapper.classList.add('active');
    });
}

if (loginLink) {
    loginLink.addEventListener('click', () => {
        wrapper.classList.remove('active');
    });
}

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
    window.location.href = "/";
});


document.querySelector("form.register").addEventListener("submit", function (e) {
    e.preventDefault();
  
    // Serialize the form data
    const formData = new FormData(this);
  
    // Send a POST request to the server
    fetch("/register", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Registration was successful, display a success message
          // You can customize this part to show the dialog.
          const dialog = document.querySelector(".success-dialog");
          dialog.style.display = "block";
        } else {
          // Handle registration failure, show an error message
          alert("Registration failed. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

  function closeDialog() {
    const dialog = document.querySelector(".success-dialog");
    dialog.style.display = "none";
  }
  


