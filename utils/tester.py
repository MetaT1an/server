from fabric import Connection
import warnings

"""
to deal with some WARNING problems due to the BUGS in paramiko mudule
"""
warnings.filterwarnings(action='ignore', module='.*paramiko.*')


# Test whether the target host can connect through ssh
def test_conn(host, username, password):
    result = True
    try:
        c = Connection(host=host, user=username, connect_kwargs={"password": password})
        c.run("whoami")
    except Exception as e:
        print("[test_conn]:", e)
        result = False
    return result
