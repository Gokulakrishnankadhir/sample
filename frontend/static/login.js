document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Send the login request to the Flask backend for authentication
    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (result.success) {
        // Redirect to the delivery page served by Flask
        window.location.href = '/delivery';  // Update the URL to point to the Flask route
    } else {
        alert(result.message);
    }
});
