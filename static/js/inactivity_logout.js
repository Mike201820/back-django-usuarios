// static/js/inactivity_logout.js

let logoutTimer;

function resetLogoutTimer() {
    clearTimeout(logoutTimer);
    logoutTimer = setTimeout(() => {
        window.location.href = "/logout/";
    }, 200000);  // 20000 ms = 20 segundos
}

window.onload = resetLogoutTimer;
window.onmousemove = resetLogoutTimer;
window.onkeypress = resetLogoutTimer;
