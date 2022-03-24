import requests

# Sends a request to a given url , and receives a json response
# 
def send_request(url, data):
    i = 0
    success = False
    while i<4:
        try:
            resp = requests.post(url=url, json=data, timeout=0.001)
        except:
            i = i+1
        else:
            break

    return success, resp
