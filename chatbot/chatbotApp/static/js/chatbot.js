function toggleInterface() {
    var interface = document.getElementById("myInterface");
    var icon = document.getElementById("toggleIcon");
    if (interface.style.display === "none") {
        interface.style.display = "block";
        icon.src = crossIconPath; // Path to your cross icon
        icon.alt = "Close Interface";
    } else {
        interface.style.display = "none";
        icon.src = openInterfaceIconPath; // Path to your open interface icon
        icon.alt = "Open Interface";
    }
}
// Add this script at the end of your body tag in your HTML document
document.getElementById("chatInput").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
         console.log("Enter key pressed. Calling sendMessage()...");
        sendMessage();
    }
});

function sendMessage() {
    var userInput = document.getElementById("chatInput").value;
    if (userInput.trim() !== '') {
        // Add user's message to chat container immediately
        addMessage('user', userInput);
        document.getElementById("chatInput").value = ''; // Clear the input field

        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        // Send user's message to backend
        fetch('/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Update chat container with response from backend
            addMessage('assistant', data.response);
        })
        .catch(error => console.error('Error:', error));
    } else {
        console.error('Error: Empty user input');
    }
}

function addMessage(role, content) {
    var chatContainer = document.getElementById("chatContainer");
    var messageDiv = document.createElement("div");
    messageDiv.classList.add("message", role);
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the latest message
}
