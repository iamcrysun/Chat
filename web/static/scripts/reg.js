 async function register() {
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch('http://localhost:16000/auth/sign-up/', {
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
                    // Если успешно, переходите на следующую страницу
                    document.location.href = 'http://localhost:16000/chat/chat/form';
                    console.log("Вход")
                } else {
                    // Обработка ошибок
                    console.error(`Error: ${response.status}`);
                    window.alert("Проверьте данные");
                }
            } catch (error) {
                // В случае ошибки вы можете обработать ее здесь
                console.error(error);
                window.alert("Проверьте данные");
            }
        }