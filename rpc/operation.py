import requests
from fabric import Connection

# to deal with some WARNING problems due to the BUGS in paramiko mudule
import warnings
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

api_url = "http://127.0.0.1:5000/scanner/{0}/status"


def get_conn(ip, username, password):
    return Connection(host=ip, user=username, connect_kwargs={'password': password})


def deploy(token, sid, ip, username, password):
    c = get_conn(ip, username, password)
    flag = True

    # check if such directory exists
    if c.run("test -d scanner/", warn=True).ok:     # exists
        c.run("rm -rf scanner/")    # remove it

    # get repository
    if c.run("git clone https://www.github.com/MetaT1an/scanner.git", warn=True).ok:
        headers = {'Authorization': token}
        requests.put(api_url.format(sid), json={'status': 1}, verify=False, headers=headers)
    else:
        flag = False

    return flag


def start(token, sid, ip, username, password):
    c = get_conn(ip, username, password)
    flag = True

    # this command should be executed in DIRECTORY scanner/
    with c.cd("scanner/"):
        if c.run("./scripts/start.sh", warn=True).failed:       # unable to start the process
            flag = False
        else:
            headers = {'Authorization': token}
            requests.put(api_url.format(sid), json={'status': 2}, verify=False, headers=headers)

    return flag


def stop(token, sid, ip, username, password):
    c = get_conn(ip, username, password)
    flag = True

    if c.run("./scanner/scripts/stop.sh", warn=True).failed:
        flag = False
    else:
        headers = {'Authorization': token}
        requests.put(api_url.format(sid), json={'status': 1}, verify=False, headers=headers)

    return flag


def undeploy(token, sid, ip, username, password):
    c = get_conn(ip, username, password)
    flag = True

    with c.cd("scanner/"):
        if c.run("./scripts/undeploy.sh", warn=True).failed:
            flag = False
        else:
            headers = {'Authorization': token}
            requests.put(api_url.format(sid), json={'status': 0}, verify=False, headers=headers)

    return flag


operation_list = [deploy, start, stop, undeploy]
