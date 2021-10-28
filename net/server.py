from flask import Flask, request
import json
import random
import requests
app = Flask(__name__)


def getId():
    return str(random.random())[2:]

class Agregator:
    countGamers = 0
    url1 = None
    url2 = None
    field1 = None
    field2 = None
    id1 = None
    id2 = None
    activeStep = 0

mainAdmin = Agregator()

@app.route("/want")
def want():
    if mainAdmin.countGamers==2:
        return json.dumps({"begin": False, "error": "Already 2 gamers connected"})

    if not "id" in request.args:
        return json.dumps({"begin": False, "error": "empty id"})

    curID = request.args.get('id')

    if mainAdmin.id1==None: # принимаем первого игрока
        mainAdmin.id1 = curID
        mainAdmin.countGamers+=1
        print("Accepted player one with url = "+mainAdmin.id1)
        return json.dumps({"begin": False, "id": mainAdmin.id1})

    elif mainAdmin.id2==None:
        if mainAdmin.id1 == curID: # удерживаем первого игрока
            return json.dumps({"begin": False})

        else: # принимаем второго игрока
            mainAdmin.id2 = curID
            mainAdmin.countGamers+=1
            print("Accepted player one with url = " + mainAdmin.id2)
            return json.dumps({"begin": True, "id": mainAdmin.id2})

    elif mainAdmin.id1 == curID: # запускаем первого игрока
        return json.dumps({"begin": True})

    else:
        print("Unrecognised want request")
        return json.dumps({"begin": False, "error": "Unrecognised want request"})

@app.route("/begin", methods=['GET'])
def begin():
    if not "id" in request.args:
        return json.dumps({"start": False, "error": "empty id"})

    if not "field" in request.args:
        return json.dumps({"start": False, "error": "empty field"})

    curID = request.args.get('id')
    field = request.args.get('field')

    if curID == mainAdmin.id1:
        mainAdmin.feild1 = field
        print("Accepted field from player 1")
        return json.dumps({"start": True})


    elif curID == mainAdmin.id2:
        mainAdmin.feild2 = field
        print("Accepted field from player 2")
        return json.dumps({"start": False})



    else:
        print("Unrecognised begin request occured")
        return json.dumps({"start": False, "error": "Unrecognised begin request"})

@app.route("/step", methods=['GET'])
def step():
    if not "id" in request.args:
        return json.dumps({"error": "empty id"})
    curID = request.args.get('id')



    if not "step" in request.args:
        return json.dumps({"error": "empty step"})
    step = request.args.get('step')

    








if __name__ == '__main__':
    app.run()


