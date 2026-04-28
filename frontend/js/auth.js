/**
 * Authentication Module
 * Handles user registration and login
 */

document.addEventListener('DOMContentLoaded', function () {
    initializeAuthPage();
});

function initializeAuthPage() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const switchTabs = document.querySelectorAll('.switch-tab');

    // Tab switching
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    switchTabs.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const tabName = this.getAttribute('href').substring(1);
            switchTab(tabName);
        });
    });

    // Form submissions
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('active');
        }
    });

    // Update forms
    document.querySelectorAll('.auth-form').forEach(form => {
        form.classList.remove('active-form');
    });

    if (tabName === 'login') {
        document.getElementById('loginForm').classList.add('active-form');
    } else if (tabName === 'register') {
        document.getElementById('registerForm').classList.add('active-form');
    }
}

async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        showLoadingState();
        const result = await api.login(username, password);

        // Redirect to dashboard
        window.location.href = '/frontend/dashboard.html';
    } catch (error) {
        showError('loginForm', error.message);
    } finally {
        hideLoadingState();
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const firstName = document.getElementById('regFirstName').value;
    const lastName = document.getElementById('regLastName').value;
    const email = document.getElementById('regEmail').value;
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('regConfirmPassword').value;

    // Validate form
    if (!email || !username || !password) {
        showError('registerForm', 'Please fill in all required fields');
        return;
    }

    if (password !== confirmPassword) {
        showError('registerForm', 'Passwords do not match');
        return;
    }

    if (password.length < 8) {
        showError('registerForm', 'Password must be at least 8 characters long');
        return;
    }

    try {
        showLoadingState();
        const result = await api.register(username, email, password, firstName, lastName);

        // Show success message
        alert('Registration successful! Redirecting to dashboard...');
        window.location.href = '/frontend/dashboard.html';
    } catch (error) {
        showError('registerForm', error.message);
    } finally {
        hideLoadingState();
    }
}

function showError(formId, message) {
    const form = document.getElementById(formId);
    const errorElement = form.querySelector('.error-message');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }

    // Auto-hide error after 5 seconds
    setTimeout(() => {
        if (errorElement) {
            errorElement.classList.remove('show');
        }
    }, 5000);
}

function showLoadingState() {
    const buttons = document.querySelectorAll('form button[type="submit"]');
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.textContent = 'Loading...';
    });
}

function hideLoadingState() {
    const buttons = document.querySelectorAll('form button[type="submit"]');
    const loginBtn = buttons[0];
    const registerBtn = buttons[1];

    if (loginBtn) {
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login';
    }
    if (registerBtn) {
        registerBtn.disabled = false;
        registerBtn.textContent = 'Register';
    }
}
