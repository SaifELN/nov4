const socket = io({transports: ['polling']});
const chatMessages = document.getElementById('chat-messages');
const usernameInput = document.getElementById('username');
const messageInput = document.getElementById('message');

function sendMessage() {
    const user = usernameInput.value;
    const message = messageInput.value;
    
    if (user && message) {
        socket.emit('send_message', { user: user, message: message });
        messageInput.value = '';
    }
}

socket.on('new_message', function(data) {
    addMessage(data);
});

function addMessage(data) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (data.user === usernameInput.value) {
        messageElement.classList.add('sent');
    }
    
    messageElement.innerHTML = `
        <div class="user">${data.user}</div>
        <div class="content">${data.message}</div>
        <div class="timestamp">${data.timestamp}</div>
    `;
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function loadMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(messages => {
            messages.reverse().forEach(addMessage);
        });
}

loadMessages();
