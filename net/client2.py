import requests
import numpy as np
from time import sleep
from icecream import ic

field = np.array([[np.random.randint(0,2) for i in range(10)] for j in range(10)])
baseUrl = "http://127.0.0.1:5000/"
urlWant = "want"
urlBegin = "begin"
urlStep = "step"
urlWaitStep = "wait_shot"
urlAns = "ans_shot"
urlWaitAns = "wait_ans"


myID = "23"

from UniversalDictClass import DictClass
class Ship(DictClass):

    def __init__(self, d=None):
        super().__init__(d)



def checkShot(step):
    x,y = step
    return "miss"


def makeStrike():
    return 1,2

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
    if "error" in data:
        print("Error from server:")
        print(data["error"])

    while not ansName in ans:
        print("Json hasn't field '" + ansName +"'")
        ans = makeGet(url,data)
    return ans[ansName], ans

def want():
    ic("want sended")
    begin = False
    while not begin:
        begin,_ = myRequest(baseUrl + urlWant, "begin", data={
            "id": myID,
        })

    return True


def begin():
    ic("begin sended")
    start,_ = myRequest(baseUrl + urlBegin, "start", data={
        "id": myID,
    })
    return start

def shot(x=0,y=0):
    step = x,y
    ic("shot", step)
    myRequest(baseUrl + urlStep, "ans", {
        "id": myID,
        "step_x": step[0],
        "step_y": step[1]
    })

def wait_shot():
    ic("wait_shot")
    ans = "wait"
    ans, data = myRequest(baseUrl + urlWaitStep, "ans", {
        "id": myID,
    })
    ic(data)
    while ans != "OK":
        ans, data = myRequest(baseUrl + urlWaitStep, "ans", {
            "id": myID,
        })

    x,y = data["step_x"], data["step_y"]
    ic(x,y)
    return x,y

def make_ans(ans="miss", ship = Ship({"zxc":3}), endGame=False):
    ic("make_ans")
    if ship!=None:
        ship = ship.__as_json__()
    data = {
        "id": myID,
        "ans": ans,
        "ship": ship,
        "endGame": endGame
    }
    ic(data)
    myRequest(baseUrl + urlAns, "ans", data)

def wait_ans():
    ic("wait_ans")
    ans = "wait"
    ans, data = myRequest(baseUrl + urlWaitAns, "ans", {
        "id": myID,
    })
    ic(data)
    while ans == "wait" or ans == "error":
        ans, data = myRequest(baseUrl + urlWaitAns, "ans", {
            "id": myID,
        })
    endGame = data["endGame"]

    ic(data)
    if ans == "miss" or data["ship"]==None:
        ship = None
    else:
        ship = Ship().__from_json__(data["ship"])
    return ans, ship, endGame


if __name__ == '__main__':
    want()
    begin()

    from time import sleep
    # for i in range(5):
    wait_shot()
    sleep(2)
    make_ans()
    shot()
    wait_ans()


    print("end")
