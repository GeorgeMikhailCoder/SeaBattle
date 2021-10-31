import requests
from time import sleep
from Ship import Ship

import os
import logging.config

class ServerConnection:

    def __id__(self):
        from random import random
        return int(random()*1_000_000_000 % 1_000_000_000)

    def __init__(self, serv_url="http://127.0.0.1:5000/"):
        self.urlWant = "want"
        self.urlBegin = "begin"
        self.urlStep = "shot"
        self.urlWaitStep = "wait_shot"
        self.urlAns = "ans_shot"
        self.urlWaitAns = "wait_ans"
        self.baseUrl = serv_url
        self.myID = self.__id__()

        self.logger = logging.getLogger("Client")
        self.logger.setLevel(logging.DEBUG)
        h = logging.FileHandler("log_client_" + str(self.myID))
        f = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        h.setFormatter(f)
        self.logger.addHandler(h)

    def __lg__(self, *args):
        s = ""
        for arg in args:
            s+= str(arg) + " "
        self.logger.info(s)

    def __lgerr__(self, *args):
        s = ""
        for arg in args:
            s+= str(arg) + " "
        self.logger.error(s)

    def __makeGet__(self, url, data=None):
        data["id"] = self.myID
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
    
    def __myRequest__(self, url, ansName, data=None):
        ans = self.__makeGet__(url, data)
        if "error" in data:
            print("Error from server:")
            print(data["error"])
    
        while not ansName in ans:
            print("Json hasn't field '" + ansName +"'")
            ans = self.__makeGet__(url,data)
        return ans[ansName], ans
    
    def want(self):
        self.__lg__("want sended")
        begin = False
        while not begin:
            begin,_ = self.__myRequest__(self.baseUrl + self.urlWant, "begin", data={
                "id": self.myID,
            })
    
        return True

    def begin(self):
        self.__lg__("begin sended")
        start,_ = self.__myRequest__(self.baseUrl + self.urlBegin, "start", data={
            "id": self.myID,
        })
        return start
    
    def shot(self, x=0,y=0):
        shot = x,y
        self.__lg__("shot", shot)
        self.__myRequest__(self.baseUrl + self.urlStep, "ans", {
            "id": self.myID,
            "step_x": shot[0],
            "step_y": shot[1]
        })
    
    def wait_shot(self):
        self.__lg__("wait_shot")
        ans = "wait"
        ans, data = self.__myRequest__(self.baseUrl + self.urlWaitStep, "ans", {
            "id": self.myID,
        })
        self.__lg__("wait_shot accepted data: ", data)
        while ans != "OK":
            ans, data = self.__myRequest__(self.baseUrl + self.urlWaitStep, "ans", {
                "id": self.myID,
            })
        self.__lg__("wait_shot accepted data: ", data)
        x,y = data["step_x"], data["step_y"]
        return x,y
    
    def make_ans(self, ans="miss", ship=None, endGame=False):
        self.__lg__("make_ans")
        if ship:
            ship = ship.__as_json__()
        data = {
            "id": self.myID,
            "ans": ans,
            "ship": ship,
            "endGame": endGame
        }
        self.__lg__("make_ans sending data: ", data)
        self.__myRequest__(self.baseUrl + self.urlAns, "ans", data)
    
    def wait_ans(self):
        self.__lg__("wait_ans")
        ans = "wait"
        ans, data = self.__myRequest__(self.baseUrl + self.urlWaitAns, "ans", {
            "id": self.myID,
        })
        self.__lg__("wait_ans accepted data: ", data)
        while ans == "wait" or ans == "error":
            ans, data = self.__myRequest__(self.baseUrl + self.urlWaitAns, "ans", {
                "id": self.myID,
            })
        endGame = data["endGame"] == "True"
    
        self.__lg__("wait_ans accepted data: ", data)
        if ans == "miss" or data["ship"]==None:
            ship = None
            self.__lg__("wait_ans ship: ", None)
        else:
            ship = Ship().__from_json__(data["ship"])
            self.__lg__("wait_ans ship: ", ship.__as_dict__())

        return ans, ship, endGame


if __name__ == '__main__':

    server = ServerConnection()
    server.want()
    server.begin()
    server.shot()
    server.wait_ans()
    server.wait_shot()
    server.make_ans()

    print("end")
