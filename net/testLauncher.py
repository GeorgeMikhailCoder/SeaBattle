from client import ServerConnection
from multiprocessing import Process
from server import runServer

def player():
    server = ServerConnection()
    server.want()
    myShot = server.begin()

    if myShot:
        server.shot()
        server.wait_ans()
        server.wait_shot()
        server.make_ans()
    else:
        server.wait_shot()
        server.make_ans()
        server.shot()
        server.wait_ans()



if __name__ == '__main__':
    s = Process(target=runServer)
    p1 = Process(target=player)
    p2 = Process(target=player)

    print("Start test")
    s.start()
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    s.kill()
    print("End test")

