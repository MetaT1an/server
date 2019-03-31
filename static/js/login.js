$(function () {
    $("#name, #pwd").focus(err_clear);
    $("#name").blur(check_name);
    $("#pwd").blur(check_password);
    $("#confirm").click(check_all);
});

function check_name() {
    let name = $("#name").val();
    let flag = true;

    if(name === ""){
        err_info("name required!");
        flag = false;
    }
    return flag;
}

function check_password() {
    let password = $("#pwd").val();
    let flag = true;

    if(password === ""){
        err_info("password required!");
        flag = false;
    }
    return flag;
}

function err_info(info) {
    $(".err").text(info)
}

function err_clear() {
    $(".err").text("")
}

function check_all() {
    let flag = check_name() && check_password();
    if(!flag){
        return false;
    } else {
        $.ajax({
           url: "/session",
           dataType: "json",
           async: true,
           type: "post",
           data: {
               "username": $("#name").val(),
               "password": $("#pwd").val()
           },
           success: function (r) {
               if(r.status){
                   sessionStorage.user = JSON.stringify(r.data);
                   window.location.href = "index.html";
               } else {
                   err_info(r.msg);
               }
           }
        });
    }
}