let usr_info = JSON.parse(sessionStorage.user);
let my_chart;
let data_set = [0, 0, 0, 0, 0];
let s_dict = {"Critical": "c", "High": "h", "Medium": "m", "Low": "l", "Info": "i"};

$(function () {
    $("#pie, #info, #vul").hide();
    get_hosts_selector();
    gen_chart();
    query_event();
});

function gen_chart() {
    let ctx = $("#chart");

    let label_set = ['Critical', 'High', 'Medium', 'low', 'info'];
    let color_set = ['#D62710', '#ED9A00', '#F9D400', '#2aa44a', '#357abd'];
    let border_width_set = [2, 2, 2, 2, 2];
    let border_color_set = ['rgba(255, 255, 255, 0.4)', 'rgba(255, 255, 255, 0.4)', 'rgba(255, 255, 255, 0.4)', 'rgba(255, 255, 255, 0.4)', 'rgba(255, 255, 255, 0.4)'];

    my_chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: label_set,
            datasets: [{
                data: data_set,
                backgroundColor: color_set,
                borderWidth: border_width_set,
                borderColor: border_color_set
            }],
        },
        options: {
            legend: {
                position: 'left'
            }
        }
    })
}

function query_event() {
    $("#query").click(function () {
        let hid = $("select").val();
        $("tbody").empty();

        $.ajax({
            url: "/" + usr_info.token + "/host/" + hid,
            type: "get",
            async: true,
            dataType: "json",
            success: function (r) {
                if(r.status){
                    data_set[0] = r.data['critical'];
                    data_set[1] = r.data['high'];
                    data_set[2] = r.data['medium'];
                    data_set[3] = r.data['low'];
                    data_set[4] = r.data['info'];

                    $("#name").text(r.data['hname']);
                    $("#status").text(r.data['status']);
                    $("#policy").text(r.data['policy']);
                    $("#start").text(r.data['start']);
                    $("#end").text(r.data['end']);
                    $("#elapse").text(r.data['elapse']);
                    $("#target").text(r.data['target']);

                    $("#pie, #info").show();
                    my_chart.update()
                }
            }
        });

        $.ajax({
            url: "/" + usr_info.token + "/host/" + hid + "/vuls",
            type: "get",
            async: true,
            dataType: "json",
            success: function (r) {
                if(r.status){
                    gen_vuls_table(r.data);
                    $("#vul").show();
                }
            }
        })
    });
}

function get_hosts_selector() {
    let tid = sessionStorage.tid;
    if(tid){
        $.ajax({
            url: "/" + usr_info.token +"/task/" + tid + "/hosts",
            type: "get",
            async: true,
            dataType: "json",
            success: function (r) {
                if(r.status){
                    gen_hosts_selector(r.data)
                }
            }
        });
    }
}

function gen_hosts_selector(hosts) {
    let selector = $("select");
    for(let i=0; i<hosts.length; ++i){
        selector.append("<option value=" + hosts[i].hid +">" + hosts[i].target + "</option>");
    }
}

function gen_vuls_table(vuls) {
    for(let i=0; i<vuls.length; ++i){

        let table_line = "<tr>\n<td><span class=" + s_dict[vuls[i]['severity']]+">"+ vuls[i]['severity'] +"</span></td>\n" +
                    "<td>" + vuls[i]['pluginname'] + "</td>\n" +
                    "<td>" + vuls[i]['pluginset'] + "</td>\n" +
                    "<td>" + vuls[i]['count'] +"</td>\n</tr>\n";

        $("tbody").append(table_line);
    }

}