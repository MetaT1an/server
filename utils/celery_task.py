import celery
import requests
import time
import threading
from utils.mail import mail_sender

broker_url = "amqp://192.168.2.12"
backend_url = "redis://192.168.2.12"
api_url = "http://127.0.0.1:5000"

app = celery.Celery(broker=broker_url, backend=backend_url)


def launch(task_id, token, email):
    # task status change
    status_url = api_url + "/{0}/task/{1}/status".format(token, task_id)
    requests.put(status_url, json={'status': 1}, verify=False)

    # 1. get all the hosts in task via given task_id
    hosts_url = api_url + "/{0}/task/{1}/hosts".format(token, task_id)
    r = requests.get(hosts_url, verify=False)
    host_list = r.json()['data']

    # ===2. create distributed tasks with celery===
    task_list = []
    for host in host_list:
        task = app.send_task("celery_task.submit_scan", [str(host['hid']), host['target'], host['policy']])
        task_list.append(task)      # hid serve as scan-task name

    # 3. listen for the completion of all celery tasks
    while task_list:
        for task in reversed(task_list):
            if not task.ready():
                print("[scan process] working...")
            else:
                task_list.remove(task)     # task which is completed
                data = task.get()

                # 1. update data to database IN NEW THREAD
                data_save_thread = threading.Thread(target=data_save, args=(data['vulns'], data['details'], token))
                data_save_thread.start()

                # 2. generate mail attachment(scan report)
                report_name = "{0}_report.html".format(data['details']['target'])
                mail_sender.add_attachment(data['report'], report_name)
            time.sleep(10)

    # 4. all task finished, email notification
    mail_sender.reliable_send(email)

    requests.put(status_url, json={'status': 2}, verify=False)


def data_save(vulns, details, token):
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
    host_put_url = api_url + "/{0}/host/{1}".format(token, hid)
    requests.put(host_put_url, json=data, verify=False)

    # create vulnerabilities information
    vul_list = vulns['list']
    for vul in vul_list:
        data = {
            'token': token,
            'hid': hid,
            'severity': vul['severity'],
            'pluginset': vul['pluginset'],
            'pluginname': vul['pluginname'],
            'count': vul['count']
        }
        vul_post_url = api_url + "/vul"
        requests.post(vul_post_url, json=data)
