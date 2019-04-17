$(function () {
    $("#ip, #username, #pwd, #pwdag").focus(err_clear);
    $("#ip").blur(check_ip);
    $("#username").blur(check_username);
    $("#pwd").blur(check_pwd);
    $("#pwdag").blur(check_pwdag);
    $("#confirm").click(check_all);
});

function check_ip() {
    let flag = true;

    if($("#ip").val() === "") {
        err_info("ip address required!");
        flag = false
    }
    return flag
}

function check_username() {
    let flag = true;
    if($("#username").val() === "") {
        err_info("username required!");
        flag = false;
    }
    return flag;
}

function check_pwd() {
    let flag = true;
    if($("#pwd").val() === "") {
        err_info("password required!");
        flag = false;
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

function err_info(info) {
    $(".err").text(info)
}

function check_all() {
    let flag = check_ip() && check_username() && check_pwd() && check_pwdag();
    if(!flag){
        return false;
    } else {
        $("#my-modal-loading").modal();
        let usr_info = JSON.parse(sessionStorage.user);
        $.ajax({
            url: "/scanner",
            headers: {"Authorization": usr_info.token},
            dataType: "json",
            async: true,
            type: "post",
            data: {
                "ip": $("#ip").val(),
                "username": $("#username").val(),
                "password": $("#pwd").val()
            },
            success: function (r) {
                $("#my-modal-loading").modal('close');
                if(r.status){
                    $("#my-alert").modal();
                    $("#ip, #username, #pwd, #pwdag").val("");
                } else {
                    err_info(r.msg);
                }
            }
        });
    }
}


function err_clear() {
    $(".err").text("")
}