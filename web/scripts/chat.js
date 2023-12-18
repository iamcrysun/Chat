function sendMessage() {
            const userInput = document.getElementById("user-input");
            const message = userInput.value;
            if (message.trim() !== "") {
                appendMessage("You: " + message);
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
                    appendMessage("Bot: " + data.message);
                });

            }
        }

        function appendMessage(message) {
            const chatMessages = document.getElementById("chat-messages");
            const messageElement = document.createElement("div");
            messageElement.textContent = message;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function logout() {
            window.location.href = 'http://localhost:16000/auth/sign-in/form';
        }