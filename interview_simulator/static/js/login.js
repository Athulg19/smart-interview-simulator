document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const formTitle = document.getElementById('form-title');
    const switchToSignup = document.getElementById('switch-to-signup');
    const switchToLogin = document.getElementById('switch-to-login');

    switchToSignup.addEventListener('click', function (e) {
        e.preventDefault();
        loginForm.classList.remove('active');
        signupForm.classList.add('active');
        formTitle.textContent = 'Sign Up';
    });

    switchToLogin.addEventListener('click', function (e) {
        e.preventDefault();
        signupForm.classList.remove('active');
        loginForm.classList.add('active');
        formTitle.textContent = 'Log In';
    });
});
