document.getElementById('deliveryForm').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way

    // Collect form data
    const destination = document.getElementById('destination').value;
    const units = document.getElementById('units').value;
    const drugType = document.getElementById('drugType').value;

    // Create a POST request to send the data to Flask backend
    try {
        const response = await fetch('/create-nft', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination, units, drugType })
        });

        const result = await response.json();

        // Handle the response
        if (result.success) {
            // If the NFT was created successfully, show a success message
            document.getElementById('status').innerText = 'NFT created successfully. Transaction Hash: ' + result.txHash;
            document.getElementById('confirmButton').innerText = 'Load Your Units';

            // Show the QR code
            const qrCodeImg = document.createElement('img');
            qrCodeImg.src = result.qrCodeUrl;  // Set the QR code URL from the response
            qrCodeImg.alt = 'QR Code for Transaction'; // Set alt text for accessibility
            
            // Append the QR code image to the status section
            const qrCodeContainer = document.getElementById('qrCodeContainer') || document.createElement('div');
            qrCodeContainer.id = 'qrCodeContainer';
            qrCodeContainer.appendChild(qrCodeImg);
            document.getElementById('status').appendChild(qrCodeContainer); // Append to status section
        } else {
            // If there was an error, display it to the user
            document.getElementById('status').innerText = 'Error creating NFT: ' + result.error;
        }
    } catch (error) {
        // If there was an error with the fetch request, display it
        document.getElementById('status').innerText = 'Error connecting to the server: ' + error.message;
    }
});