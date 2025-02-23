function addMessage(message, isUser) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    if (isUser) {
        messageDiv.textContent = message;
    } else {
        // Parse markdown for bot messages
        messageDiv.innerHTML = marked.parse(message);
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showThinking() {
    const messagesDiv = document.getElementById('chat-messages');
    const thinkingDiv = document.createElement('div');
    thinkingDiv.className = 'thinking';
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;
    messagesDiv.appendChild(thinkingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeThinking() {
    const thinkingDiv = document.getElementById('thinking-indicator');
    if (thinkingDiv) {
        thinkingDiv.remove();
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, true);
        input.value = '';
        input.disabled = true;
        sendButton.disabled = true;
        
        showThinking();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            removeThinking();
            addMessage(data.response, false);
        } catch (error) {
            removeThinking();
            addMessage('Sorry, there was an error processing your request.', false);
        }
        
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
}

document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
