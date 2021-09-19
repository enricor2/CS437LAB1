import move
import time

travelTime = .25

def getTravelTime():
    global travelTime
    move.move(50,'forward','no',0.8)
    time.sleep(travelTime)
    move.motorStop()
    print("Enter cms traveled forward: ")
    dist = float(input())
    travelTime = travelTime * 1 / dist
    if dist > 1:
        move.move(50,'backward','no',0.8)
        time.sleep(travelTime*dist)
    move.motorStop()


def move1():
    global travelTime
    move.move(50,'forward','no',0.8)
    time.sleep(travelTime)
    move.motorStop()