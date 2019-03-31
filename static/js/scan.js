//1. query the policies for later appending operation
var selector;
get_policy_selector();
var time = 3;   //countdown time

$(function () {
    add_target_event();
    $(".more").click(add_target_event);
    $(".create").click(submit_event);
    $(".less").click(del_last_line);
});

function get_policy_selector() {
    selector = "<select data-am-selected>" + "\n";
    $.ajax({
        async: true,
        type: "get",
        url: "/policies",
        success: function (r) {
            if(r.status){
                $.each(r.data, function () {
                    selector += "<option value=" + this.pname + ">" + this.pname + "</option>\n";
                });
                selector += "</select>\n";
            }
        }
    });
}

function add_target_event() {

    // append a new line
    $(".main-m").append(get_new_line());

    // reload related js file
    $.ajax({
        async: true,
        type: "get",
        url: "http://cdn.amazeui.org/amazeui/2.7.2/js/amazeui.min.js",
        dataType: "script",
    });
}

function get_new_line() {
    return $("<div class=target>\n" +
                "<label>Target: </label>\n" +
                "<input type=text class=t-ip placeholder='ip address or domain name'>" +
                "<label>Policy: </label>\n" +
        "<div class=policy>\n" +
        selector +
        "</div>\n" + "</div>")
}

function del_last_line() {
    $(".main-m").children(".target:last-child").remove();
}

function submit_event() {
    let err_box = $(".err");

    if(!check_task_name()){
        err_box.text("Task name required!");
    } else if(!check_name_len()){
        err_box.text("Task-name length < 30!");
    } else if(!check_ips()){
        err_box.text("missing scan target!");
    } else {
        err_box.text("");
        let ips = [];
        let policies = [];
        let sub_tasks = [];

        // 1. to get all the ips
        let $targets = $(".target input");
        $.each($targets, function () {
            ips.push($(this).val());
        });

        // 2. to get all the policies
        let $selections = $(".target select");
        $.each($selections, function () {
            policies.push($(this).val())
        });

        // 3. generate sub-task entity
        for(let i = 0; i < ips.length; ++i){
            sub_tasks.push({"target": ips[i], "policy": policies[i]});
        }

        // 4. prepare data
        let usr_info = JSON.parse(sessionStorage.user);

        // 5. submit
        $.ajax({
            url: "/task",
            dataType: "json",
            async: true,
            type: "post",
            data: {
                "token": usr_info.token,
                "tname": $("#t-name").val(),
                "hosts": JSON.stringify(sub_tasks)      //convert to python list in backend
            },
            success: function (r) {
                if(r.status){
                    success_style();
                    to_task_page();
                }
            }
        })
    }

}

function check_ips() {
    let $targets = $(".target input");
    let flag = true;

    if($targets.length === 0){
        flag = false;
    } else {
        $.each($targets, function () {
            if($(this).val() === "") {
                flag = false;
            }
        });
    }
    return flag;
}

function check_task_name() {
    return $("#t-name").val() !== "";
}

function check_name_len() {
    return $("#t-name").val().length <= 30;
}

function to_task_page() {
    setTimeout(to_task_page, 1000);
    if(time > 0){
        let info = "Redirect to task page after " + time + "s";
        err_info(info);
        time--;
    } else {
        window.location.href = "task.html";
    }
}

function success_style() {
    let info_box = $(".err");
    info_box.css({
        color: "#fff",
        background: "#89ee90"
    });
}

function err_info(info) {
    $(".err").text(info);
}

