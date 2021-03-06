from flask import Flask, request
import json
from icecream import ic
import os
import logging.config

class ClientAcceptor:
    app = None
    answers = {
        "kill": "kill",
        "injured": "get",
        "miss": "miss",
        "retry": "retry",
    }

    class Agregator:
        countGamers = 0
        activeGamer = None
        gamers = {}
        shot = None
        endGame = False
        data = None

    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule("/want", "want", self.want)
        self.app.add_url_rule("/begin", "begin", self.begin)
        self.app.add_url_rule("/shot", "shot", self.shot)
        self.app.add_url_rule("/wait_shot", "wait_shot", self.wait_shot)
        self.app.add_url_rule("/ans_shot", "ans_shot", self.ans_shot)
        self.app.add_url_rule("/wait_ans", "wait_ans", self.wait_ans)
        self.mainAdmin = self.Agregator()

        self.__log_file_path__ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_log.conf')
        logging.config.fileConfig(self.__log_file_path__)
        self.logger = logging.getLogger("Server")
        self.logger.info("\n\n")
        self.logger.info("Begin session")

    def run(self):
        self.app.run()

    def __lg__(self, *args):
        curID = args[0]

        s = str(curID).ljust(10," ")

        if curID in self.mainAdmin.gamers:
            s = "player" + str(self.mainAdmin.gamers[curID]["n"]) + " "

        for arg in args[1:]:
            s+= str(arg) + " "
        self.logger.info(s)

    def __switchActive__(self, curID):
        x = self.mainAdmin.gamers.copy()
        x.pop(curID)

        z = x.keys()
        k=[a for a in z][0]
        newID = self.mainAdmin.gamers[k]["id"]
        return newID

    def want(self):
        if not "id" in request.args:
            return json.dumps({"begin": False, "error": "empty id"})

        curID = request.args.get('id')
        self.__lg__(curID, "want")


        if self.mainAdmin.countGamers==0: # принимаем первого игрока
            self.mainAdmin.gamers[curID] = {"id": curID,
                                       "n": 1}
            self.mainAdmin.countGamers+=1
            self.mainAdmin.activeGamer = curID
            self.__lg__(curID, str(curID)+" accepted as player one")
            return json.dumps({"begin": False, "id": curID})

        elif self.mainAdmin.countGamers==1:
            if curID in self.mainAdmin.gamers.keys(): # удерживаем первого игрока
                return json.dumps({"begin": False})

            else: # принимаем второго игрока
                self.mainAdmin.gamers[curID] = {"id": curID,
                                           "n": 2}
                self.mainAdmin.countGamers+=1
                self.__lg__(curID, str(curID)+" accepted as player two")
                self.__lg__(curID, "Launched secound player")
                return json.dumps({"begin": True, "id": curID})

        elif curID in self.mainAdmin.gamers.keys(): # запускаем первого игрока
            self.__lg__(curID, "Launched first player")
            return json.dumps({"begin": True})

        else:
            print("Unrecognised want request")
            return json.dumps({"begin": False, "error": "Unrecognised want request"})

    def begin(self):
        if not "id" in request.args:
            return json.dumps({"start": False, "error": "empty id"})
        curID = request.args.get('id')

        self.__lg__(curID, "begin")
        return json.dumps({"start": curID == self.mainAdmin.activeGamer})

    def shot(self):
        if not "id" in request.args:
            return json.dumps({"error": "empty id"})
        curID = request.args.get('id')
        self.__lg__(curID, "shot",request.args.get('step_x'), request.args.get('step_y'))

        if curID == self.mainAdmin.activeGamer:
            if not "step_x" in request.args:
                return json.dumps({"error": "empty step"})
            self.mainAdmin.shot = (request.args.get('step_x'), request.args.get('step_y'))

            return json.dumps({"ans": "OK"})
        else:
            return json.dumps({"error": "wait enemy shot from the '/waitstep' url"})

    def wait_shot(self):
        if not "id" in request.args:
            return json.dumps({"error": "empty id"})
        curID = request.args.get('id')
        self.__lg__(curID, "wait_shot")

        if curID != self.mainAdmin.activeGamer:
            if self.mainAdmin.shot != None:
                step = self.mainAdmin.shot
                self.mainAdmin.shot = None
                self.__lg__(curID, "wait_shot", f"shot = {step}")
                return json.dumps({"ans": "OK", "step_x": step[0], "step_y": step[1]})
            else:
                return json.dumps({"ans": "wait"})
        else:
            return json.dumps({"ans": "error", "error": "It is your step. Make shot in '/shot' url"})

    def ans_shot(self):
        if not "id" in request.args:
            return json.dumps({"error": "empty id"})
        curID = request.args.get('id')
        self.__lg__(curID, "ans_shot")

        if curID != self.mainAdmin.activeGamer:
                ans = request.args.get('ans')

                if request.args.get('endGame')==True:
                    self.mainAdmin.endGame = True
                    self.mainAdmin.countGamers=0
                    self.__lg__(curID, "End Game")

                if ans == self.answers["miss"]:
                    self.mainAdmin.activeGamer = curID

                self.__lg__(curID, "ans_shot: request.args", request.args)
                self.mainAdmin.data = {a[0]:a[1] for a in zip(request.args.keys(), request.args.values())}
                self.__lg__(curID, "ans_shot: mainAdmin.data: ", self.mainAdmin.data)
                return json.dumps({"ans": "Answer recieved"})
        else:
            return json.dumps({"ans": "error", "error": "wait answer in 'wait_ans' url"})

    def wait_ans(self):
        if not "id" in request.args:
            return json.dumps({"error": "empty id"})
        curID = request.args.get('id')
        self.__lg__(curID, "wait_ans")

        if self.mainAdmin.data != None:
            tmpDict = self.mainAdmin.data
            self.mainAdmin.data = None
            self.__lg__(curID, "wait_ans: ans send: ", tmpDict)
            return json.dumps(tmpDict)
        else:
            return json.dumps({"ans": "wait"})

def runServer():
    s = ClientAcceptor()
    s.run()

if __name__ == '__main__':
    s=ClientAcceptor()
    s.run()


