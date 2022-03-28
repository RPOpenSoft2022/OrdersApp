import requests

# Sends a request to a given url , and receives a json response
# 
def send_request_post(url, data):
    i = 0
    success = False
    resp = None
    while i<4:
        try:
            resp = requests.post(url=url, json=data, timeout=1)
        except:
            i = i+1
        else:
            success = True
            break

    return success, resp


def send_request_get(url):
    i = 0
    success = False
    resp = None
    while i<4:
        try:
            resp = requests.get(url=url, timeout=1)
        except:
            i = i+1
        else:
            success = True
            break

    return success, resp

