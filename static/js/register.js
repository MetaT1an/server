var time = 3;

$(function () {
    $("#name, #email, #pwd, #pwdag").focus(err_clear);
    $("#name").blur(check_name);
    $("#email").blur(check_email);
    $("#pwd").blur(check_pwd);
    $("#pwdag").blur(check_pwdag);
    $("#register").click(check_all)

});

function check_name() {
    let name = $("#name").val();
    let flag = true;

    if(name === ""){
        err_info("name required!");
        flag = false
    } else if(name.length < 4 || name.length > 10){
        err_info("name: 4~10 letters length");
        flag = false;
    }
    return flag;
}

function check_email() {
    let flag = true;
    let email = $("#email").val();

    if(email === ""){
        err_info("email required!");
        flag = false;
    } else if(!email.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/)){
        err_info("Invalid email address!");
        flag = false
    }
    return flag
}

function check_pwd() {
    let flag = true;

    if($("#pwd").val() === ""){
        flag = false;
        err_info("password required!");
    }
    return flag;
}

function check_pwdag() {
    let flag = true;
    if($("#pwd").val() !== $("#pwdag").val()){
        err_info("password dose not match!");
        flag = false;
    }
    return flag;
}

function check_all() {
    let flag = check_name() && check_email() && check_pwd() && check_pwdag();
    if(!flag){
        return false;
    } else {
        let name = $("#name").val();
        let email = $("#email").val();
        let pwd = $("#pwd").val();

        $.ajax({
            url: "http://127.0.0.1:5000/user",
            dataType: "json",
            async: true,
            type: "post",
            data: {
                "username": name,
                "email": email,
                "password": pwd
            },
            success: function (r) {
                if(r.status){
                    success_style();
                    sessionStorage.user = JSON.stringify(r.data);
                    to_index();
                } else {
                    err_info(r.msg);
                }
            }
        });
    }
}

function err_info(info) {
    $(".err").text(info)
}

function err_clear() {
    $(".err").text("")
}

function success_style() {
    let info_box = $(".err");
    info_box.css({
        color: "#fff",
        background: "#89ee90"
    });
}

function to_index() {
    setTimeout(to_index, 1000);
    if(time > 0){
        let info = "Redirect to home page after " + time + "s";
        err_info(info);
        time--;
    } else {
        window.location.href = "index.html";
    }
}