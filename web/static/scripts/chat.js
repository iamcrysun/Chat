function sendMessage() {
            const userInput = document.getElementById("user-input");
            const message = userInput.value;
            if (message.trim() !== "") {
                appendMessage("<strong>You: </strong>" + message);
                userInput.value = "";
                // Send the message to the server

                fetch('http://localhost:16000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                }).then(response => response.json())
                .then(data => {
                    appendMessage("<strong>Bot: </strong>" + data.message);
                    appendMessage("<br>");
                });

            }
        }

        function appendMessage(message) {
            const chatMessages = document.getElementById("chat-messages");
            const messageElement = document.createElement("div");
            messageElement.innerHTML = message;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function logout() {
            window.location.href = 'http://localhost:16000/auth/sign-in/form';
        }

function loadChatData() {
    fetch('http://localhost:16000/chat/all/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(chat => processChat(chat));
    })
    .catch(error => console.error('Error loading chat data:', error));
}

function processChat(chat) {
    // Здесь chat - это один элемент из списка
    const question = chat.question;
    const answer = chat.answer;


    appendMessage("<strong>You: </strong>" + question);
    appendMessage("<strong>Bot: </strong>" + answer );
    appendMessage("<br>");
}