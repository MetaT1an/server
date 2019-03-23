$(function () {
    if (sessionStorage.length !== 0) {
        let usr_info = JSON.parse(sessionStorage.user);
        $("#usr").text(usr_info.username);
    } else {
        window.location.href = "login.html";
    }
});