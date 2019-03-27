let usr_info = JSON.parse(sessionStorage.user);

$(function () {
    get_tasks();
    task_start_event();
    task_delete_event();
    task_detail_event();
});

function get_tasks() {
    $.ajax({
        url: "http://127.0.0.1:5000/" + usr_info.token + "/tasks",
        dataType: "json",
        async: true,
        type: "get",
        success: function (r) {
            if(r.status){
                gen_tasks(r.data);
            }
        }
    })
}

function gen_tasks(tasks) {
    for(let i = 0; i < tasks.length; ++i){
        let status = "";    // status to show

        if(tasks[i].status === 0){
            status = "ready";
        } else if(tasks[i].status === 1){
            status = "running";
        } else {
            status = "completed"
        }

        let task_item = "<div class=item>\n" +
            "                <span class=tname>" + tasks[i].tname + "</span>\n" +
            "                <span class=date>" + tasks[i].date + "</span>\n" +
            "                <span class=state>" + status + "</span>\n" +
            "                <span class=op>\n";

        if(tasks[i].status === 0){ //ready
            task_item += "<button class='am-btn am-btn-success am-radius am-btn-xs start' name=" + tasks[i].tid +">start</button>\n" +
                "<button class='am-btn am-btn-danger am-radius am-btn-xs del' name=" + tasks[i].tid +">delete</button>"
        } else if(tasks[i].status === 1){//running
            task_item += "<div class=\"am-progress am-progress-striped am-active\">\n" +
                "<div class=\"am-progress-bar am-progress-bar-success\"  style=\"width: 40%\"></div>\n" +
                "</div>"
        } else { //status == 2;  completed
            task_item += "<button class='am-btn am-btn-secondary am-radius am-btn-xs detail' name=" + tasks[i].tid + ">details</button>\n" +
                "<button class='am-btn am-btn-danger am-radius am-btn-xs del' name=" + tasks[i].tid + ">delete</button>"
        }
        task_item += "</span>\n</div>";
        $(".content").append(task_item);
    }
}

function task_start_event() {
    $("body").delegate(".start", "click", function () {
        let $start_btn = $(this);
        let tid = $start_btn.attr("name");
        let progress_bar = "<div class=\"am-progress am-progress-striped am-active\">\n" +
            "<div class=\"am-progress-bar am-progress-bar-success\"  style=\"width: 40%\"></div>\n"+
            "</div>";
        $.ajax({
            url: "http://127.0.0.1:5000/" + usr_info.token + "/task/" + tid,
            dataType: "json",
            async: true,
            type: "put",
            success: function (r) {
                if(r.status){
                    $start_btn.parent().html(progress_bar);
                } else {
                    // modal
                }
            }
        })
    })
}

function task_delete_event() {
    $("body").delegate(".del", "click", function () {
        let $del_btn = $(this);
        let tid = $del_btn.attr("name");

        $("#my-confirm").modal({
            onConfirm: function () {
                $.ajax({
                    url: "http://127.0.0.1:5000/" + usr_info.token + "/task/" + tid,
                    dataType: "json",
                    async: true,
                    type: "delete",
                    success: function (r) {
                        if(r.status){
                            $del_btn.parents(".item")[0].remove()
                        }
                    }
                })
            },
            conCancel: function () {
                // pass
            }
        })
    })
}

function task_detail_event() {
    $("body").delegate(".detail", "click", function () {
        let $detail_btn = $(this);

        sessionStorage.tid = $detail_btn.attr("name");
        window.location.href = "report.html"
    })
}

