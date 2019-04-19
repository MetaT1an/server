let usr_info = JSON.parse(sessionStorage.user);

$(function () {
    get_scanners();
    deploy_event();
    start_event();
    stop_event();
    delete_event();
    undeploy_event();
});

function get_scanners() {
    $.ajax({
        url: "/scanners",
        headers: {"Authorization": usr_info.token},
        dataType: "json",
        async: true,
        type: "get",
        success: function (r) {
            if(r.status){
                gen_scanners(r.data);
            } else {
                show_alert(r.msg)
            }
        }
    });
}

function gen_scanners(scanners) {
    for(let i = 0; i < scanners.length; ++i){
        let status = "";

        if(scanners[i].status === 0){
            status = "Undeployed";
        } else if(scanners[i].status === 1){
            status = "Stopped";
        } else {
            status = "Working..."
        }

        let scanner_item = "<div class=item>\n" +
            "                <span class=ip>" + scanners[i].ip + "</span>\n" +
            "                <span class=state>" + status + "</span>\n" +
            "                <span class=op>\n";

        if(scanners[i].status === 0){
            scanner_item += "<button class='am-btn am-btn-primary am-radius am-btn-xs deploy' name=" + scanners[i].sid +">deploy</button>\n" +
                "<button class='am-btn am-btn-danger am-radius am-btn-xs delete' name=" + scanners[i].sid +">delete</button>"
        } else if(scanners[i].status === 1){
            scanner_item += "<button class='am-btn am-btn-success am-radius am-btn-xs start' name=" + scanners[i].sid +">start</button>\n" +
                "<button class='am-btn am-btn-warning am-radius am-btn-xs undeploy' name=" + scanners[i].sid +">undeploy</button>"
        } else {
            scanner_item += "<button class='am-btn am-btn-warning am-radius am-btn-xs stop' name=" + scanners[i].sid +">stop</button>\n"
        }

        scanner_item += "</span>\n</div>";
        $(".content").append(scanner_item)
    }
}

function show_alert(msg) {
    $("#msg").text(msg);
    $("#my-alert").modal()
}

function deploy_event() {
    $("body").delegate(".deploy", "click", function () {
        $("#my-modal-loading").modal();     // show loading modal
        let sid = $(this).attr("name");
        remote_operation(sid, 0)
    })
}

function start_event() {
    $("body").delegate(".start", "click", function () {
        $("#my-modal-loading").modal();
        let sid = $(this).attr("name");
        remote_operation(sid, 1)
    })
}

function stop_event() {
    $("body").delegate(".stop", "click", function () {
        $("#my-modal-loading").modal();
        let sid = $(this).attr("name");
        remote_operation(sid, 2)
    })
}

function undeploy_event() {
    $("body").delegate(".undeploy", "click", function () {
        $("#my-modal-loading").modal();
        let sid = $(this).attr("name");
        remote_operation(sid, 3)
    })
}

function delete_event() {
    $("body").delegate(".delete", "click", function () {
        $("#my-confirm").modal({
            onConfirm: function () {
                $.ajax({
                    url: "/scanner/" + $(this).attr("name"),
                    headers: {'Authorization': usr_info.token},
                    dataType: "json",
                    async: true,
                    type: "delete",
                    success: function (r) {
                        $("#my-modal-loading").modal('close');
                        if(r.status){
                            $(".content").empty();
                            get_scanners();
                        } else {
                            show_alert(r.msg)
                        }
                    }
                })
            }
        }); //modal

    })
}

function remote_operation(sid, op_code) {
    $.ajax({
        url: "/scanner/" + sid,
        headers: {'Authorization': usr_info.token},
        dataType: "json",
        async: true,
        type: "put",
        data: {'op_code': op_code},
        success: function (r) {
            if(r.status){
                $(".content").empty();
                get_scanners();
            } else {
                show_alert(r.msg)
            }
            $("#my-modal-loading").modal('close');
        }
    })
}