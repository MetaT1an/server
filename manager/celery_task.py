import celery
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from manager.mail import MailSender

broker_url = "amqp://192.168.2.12"
backend_url = "redis://192.168.2.12"
api_url = "http://127.0.0.1:5000"

app = celery.Celery(broker=broker_url, backend=backend_url)
executor = ThreadPoolExecutor(2)


def launch(task_id, token, email):
    mail_sender = MailSender()
    headers = {'Authorization': token}

    # task status change
    status_url = api_url + "/task/{0}/status".format(task_id)
    requests.put(status_url, json={'status': 1}, verify=False, headers=headers)

    # 1. get all the hosts in task via given task_id
    hosts_url = api_url + "/task/{0}/hosts".format(task_id)
    r = requests.get(hosts_url, verify=False, headers=headers)
    host_list = r.json()['data']

    # ===2. create distributed tasks with celery===
    task_list = []
    for host in host_list:
        task = app.send_task("celery_task.submit_scan", [str(host['hid']), host['target'], host['policy']])
        task_list.append(task)      # hid serve as scan-task name

    # 3. listen for the completion of all celery tasks
    # === for the usage of time cost testing ===
    start_time = time.time()

    while task_list:
        for task in reversed(task_list):
            if not task.ready():
                print("[scan process] working...")
            else:
                task_list.remove(task)     # task which is completed
                data = task.get()

                # 1. update data to database ThreadPoolExecutor
                executor.submit(data_save, data['vulns'], data['details'], headers)

                # 2. generate mail attachment(scan report)
                report_name = "{0}_report.html".format(data['details']['target'])
                mail_sender.add_attachment(data['report'], report_name)
        time.sleep(5)

    # === for the usage of time cost testing ===```````
    span = time.time() - start_time
    print("\n[time cost] {0}min {1}s\n".format(span // 60, span % 60))

    # 4. all task finished, email notification
    mail_sender.reliable_send(email)

    requests.put(status_url, json={'status': 2}, verify=False, headers=headers)


def data_save(vulns, details, headers):
    hid = details['name']

    # update host information
    data = {
        'status': details['status'],
        'start': details['start'],
        'end': details['end'],
        'elapse': details['elapse'],
        'critical': vulns['critical_num'],
        'high': vulns['high_num'],
        'medium': vulns['medium_num'],
        'low': vulns['low_num'],
        'info': vulns['info_num']
    }
    host_put_url = api_url + "/host/{0}".format(hid)
    requests.put(host_put_url, json=data, verify=False, headers=headers)

    # create vulnerabilities information
    vul_list = vulns['list']
    for vul in vul_list:
        data = {
            'hid': hid,
            'severity': vul['severity'],
            'pluginset': vul['pluginset'],
            'pluginname': vul['pluginname'],
            'count': vul['count']
        }
        vul_post_url = api_url + "/vul"
        requests.post(vul_post_url, json=data, headers=headers)
