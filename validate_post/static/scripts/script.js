var attempts = 0
function generateCaptcha() {
    var captcha = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (var i = 0; i < 6; i++) {
        captcha += characters.charAt(Math.floor(Math.random() * characters.length));
    }

    document.getElementById('captcha').innerText = captcha;
}
function validateCaptcha(id) {
    var userInput = document.getElementById('captchaInput').value;
    var generatedCaptcha = document.getElementById('captcha').innerText;
    if (userInput === generatedCaptcha && attempts < 3) {
        alert('Captcha válido');
        document.getElementById("form_worker_block_" + id).submit();
    } else {
        attempts++;
        if (attempts >= 3) {
            attempts = 0;
            alert('Captcha incorrecto. Numero de intentos maximos alcanzado');
            document.getElementById("form_captcha_failed_" + id).submit(); 
        } else {
            alert('Captcha incorrecto. Por favor, inténtalo de nuevo.');
            generateCaptcha(); 
        }
    }
}
window.onload = generateCaptcha;