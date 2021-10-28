import requests
import numpy as np
from time import sleep


field = np.array([[np.random.randint(0,2) for i in range(10)] for j in range(10)])
baseUrl = "http://127.0.0.1:5000/"
urlWant = "want"
urlBegin = "begin"
myID = "12"

def makeGet(url, data=None):
    data["id"] = myID
    while True:
        try:
            ans = requests.get(url, params=data)
            sleep(1)
            if ans.status_code!=200:
                print("Some errors in connection. Next try in 1 secound")
                continue
            res = ans.json()
            break
        except:
            print("Some error while parsing json")
    return res

def myRequest(url, ansName, data=None):
    ans = makeGet(url,data)
    while not ansName in ans:
        print("Json hasn't field '" + ansName +"'")
        ans = makeGet(url,data)
    return ans[ansName]

def want():
    begin = False
    while not begin:
        begin = myRequest(baseUrl + urlWant, "begin", data={
            "id": myID,
        }) == "True"

    return True


def begin():
    start = myRequest(baseUrl + urlBegin, "start", data={
        "id": myID,
        "field": field,
    }) == "True"
    return start

def game():
    want()
    myStart = begin()
    if myStart:
        print("I am starting!")


if __name__ == '__main__':
    begin = myRequest(baseUrl + urlWant, "begin", data={
        "id": myID,
    })

    start = myRequest(baseUrl + urlBegin, "start", data={
        "id": myID,
        "field": field,
    })

    print(begin)
    print(start)