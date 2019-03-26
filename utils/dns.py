from dns import resolver


def valid_host(host):
    flag = True
    try:
        resolver.query(host, "A")
    except Exception:
        flag = False
    return flag
