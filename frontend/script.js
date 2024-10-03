const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', userMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        userMessage();
    }
});

function userMessage() {
    const message = userInput.value.trim();
    if (message) {
        appendMessage('You', message, 'user-message');
        userInput.value = '';
        fetchResponse(message);
    }
}

function appendMessage(sender, message, className) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${className}`;
    messageElement.innerHTML = `
        <b>${sender}</b> <br>
        <p>${message}</p>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function fetchResponse(message) {
    try {
        const response = await fetch('/chat', {
            method: 'POST', // post request to send user message
            headers: {
                'Content-Type': 'application/json', // specify type to expect
            },
            body: JSON.stringify({ message }),
        });
        const data = await response.json();
        appendMessage('Bot', data.response, 'bot-message');

    } catch (error) {
        appendMessage('Bot', 'Sorry, there was an error processing your request.');
    }
}