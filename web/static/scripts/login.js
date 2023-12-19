async function login() {
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch('http://localhost:16000/sign-in/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    }),
                });

                if (response.ok) {
                    // Если успешно, переход на следующую страницу
                    window.location.href = 'chat.html';
                } else {
                    // Обработка ошибок
                    console.error(`Error: ${response.status}`);
                }
            } catch (error) {

                console.error(error);
            }
        }