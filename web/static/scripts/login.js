async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch('http://localhost:16000/auth/sign-in/', {
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
            document.location.href = 'http://localhost:16000/chat/chat/form';
            console.log("Вход")
        } else {
            // Обработка ошибок
            console.error(`Error: ${response.status}`);
            window.alert("Произошла ошибка входа. Пожалуйста, проверьте свои учетные данные.");
        }
    } catch (error) {
        console.error(error);
        window.alert("Произошла ошибка входа. Пожалуйста, повторите попытку позже.");
    }
}