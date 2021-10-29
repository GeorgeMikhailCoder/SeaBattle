from flask import Flask, request
import json
from icecream import ic
app = Flask(__name__)



def checkStep(step, field):
    x,y = step

    return "miss"

answers = {
    "kill":"kill",
    "injured":"get",
    "miss":"miss",
    "retry":"retry",
}

class Agregator:
    countGamers = 0
    activeGamer = None
    gamers = {}
    step = None
    ans_step = None
    endGame = False



mainAdmin = Agregator()

@app.route("/want")
def want():
    if not "id" in request.args:
        return json.dumps({"begin": False, "error": "empty id"})

    curID = request.args.get('id')

    if mainAdmin.countGamers==0: # принимаем первого игрока
        mainAdmin.gamers[curID] = {"id": curID,
                                   "n": 1}
        mainAdmin.countGamers+=1
        mainAdmin.activeGamer = curID
        print("Accepted player one with url = "+curID)
        return json.dumps({"begin": False, "id": curID})

    elif mainAdmin.countGamers==1:
        if curID in mainAdmin.gamers.keys(): # удерживаем первого игрока
            return json.dumps({"begin": False})

        else: # принимаем второго игрока
            mainAdmin.gamers[curID] = {"id": curID,
                                       "n": 2}
            mainAdmin.countGamers+=1
            print("Accepted player two with url = " + curID)
            print("Launched secound player")
            return json.dumps({"begin": True, "id": curID})

    elif curID in mainAdmin.gamers.keys(): # запускаем первого игрока
        print("Launched first player")
        return json.dumps({"begin": True})

    else:
        print("Unrecognised want request")
        return json.dumps({"begin": False, "error": "Unrecognised want request"})

# up works

@app.route("/begin", methods=['GET'])
def begin():
    if not "id" in request.args:
        return json.dumps({"start": False, "error": "empty id"})
    curID = request.args.get('id')
    return json.dumps({"start": curID == mainAdmin.activeGamer})




@app.route("/step", methods=['GET'])
def step():
    if not "id" in request.args:
        return json.dumps({"error": "empty id"})
    curID = request.args.get('id')


    if curID == mainAdmin.activeGamer:
        if not "step" in request.args:
            return json.dumps({"error": "empty step"})
        mainAdmin.step = request.args.get('step')

        return json.dumps({"ans": "OK"})
    else:
        return json.dumps({"error": "wait enemy shot from the '/waitstep' url"})

@app.route("/wait_shot", methods=['GET'])
def wait_shot():
    if not "id" in request.args:
        return json.dumps({"error": "empty id"})
    curID = request.args.get('id')

    ic(mainAdmin.activeGamer)
    if curID != mainAdmin.activeGamer:
        if mainAdmin.step != None:
            step = mainAdmin.step
            mainAdmin.step = None
            print(f"")
            return json.dumps({"ans": "OK", "step": step})
        else:
            return json.dumps({"ans": "wait", "step":None})
    else:
        return json.dumps({"ans": "error", "error": "It is your step. Make shot in '/shot' url"})

def switchActive(curID):
    x = mainAdmin.gamers.copy()
    x.pop(curID)

    z = x.keys()
    k=[a for a in z][0]
    newID = mainAdmin.gamers[k]["id"]
    return newID


@app.route("/ans_shot", methods=['GET'])
def ans_shot():
    if not "id" in request.args:
        return json.dumps({"error": "empty id"})
    curID = request.args.get('id')

    if curID != mainAdmin.activeGamer:
            ans = request.args.get('ans')

            if 'endGame' in request.args:
                mainAdmin.endGame = True

            if ans == answers["miss"]:
                mainAdmin.activeGamer = curID
                ic(curID, mainAdmin.activeGamer)

            mainAdmin.ans_step = ans
            return json.dumps({"ans": "Answer recieved"})
    else:
        return json.dumps({"ans": "error", "error": "wait answer in 'wait_ans' url"})


@app.route("/wait_ans", methods=['GET'])
def wait_ans():
    if not "id" in request.args:
        return json.dumps({"error": "empty id"})
    curID = request.args.get('id')

    if mainAdmin.ans_step != None:
        ans = {"ans": mainAdmin.ans_step}

        if mainAdmin.endGame:
            ans["endGame"]=True

        return json.dumps(ans)
    else:
        return json.dumps({"ans": "wait"})



if __name__ == '__main__':
    app.run()


