import move
import time

rotationTime = .0165
direction = 1 # 1-U 2-D 3-R 4-L

def getRotationTime():
    global rotationTime
    for x in range(360):
        rotateDegRight()
    print("Enter degrees rotated: ")
    rotation = float(input())
    rotationTime = rotationTime * 360 / rotation
    if rotation > 360:
        for x in range(int(rotation)-360):
            rotateDegLeft()
    elif rotation < 360:
        for x in range(360-int(rotation)):
            rotateDegRight()
    print("Enter degrees till 360 (negative if overshot): ")
    rotation = float(input())
    if rotation < 0:
        for x in range(-int(rotation)):
            rotateDegLeft()
    elif rotation > 0:
        for x in range(int(rotation)):
            rotateDegRight()

def rotateDegRight():
        move.move(100,'no','right',0.8)
        time.sleep(rotationTime)
        move.motorStop()
        time.sleep(.05)

def rotateDegLeft():
        move.move(100,'no','left',0.8)
        time.sleep(rotationTime)
        move.motorStop()
        time.sleep(.05)

def turn(nextStep):
    global direction
    print("turn", nextStep, direction)
    if direction == 1:                    #F
        if nextStep == [1,0]:       #F
            return
        elif nextStep == [0,1]:     #R
            for x in range(90):
                rotateDegRight()
            direction = 3
            return
        elif nextStep == [-1,0]:    #B
            for x in range(180):
                rotateDegRight()
            direction = 2
            return
        elif nextStep == [0,-1]:    #L
            for x in range(90):
                rotateDegLeft()
            direction = 4
            return
    elif direction == 2:                  #B
        if nextStep == [1,0]:       #F
            for x in range(180):
                rotateDegRight()
            direction = 1
            return
        elif nextStep == [0,1]:     #R
            for x in range(90):
                rotateDegLeft()
            direction = 3
            return
        elif nextStep == [-1,0]:    #B
            return
        elif nextStep == [0,-1]:    #L
            for x in range(90):
                rotateDegRight()
            direction = 4
            return
    elif direction == 3:                  #R
        if nextStep == [1,0]:       #F
            for x in range(90):
                rotateDegLeft()
            direction = 1
            return
        elif nextStep == [0,1]:     #R
            return
        elif nextStep == [-1,0]:    #B
            for x in range(90):
                rotateDegRight()
            direction = 2
            return
        elif nextStep == [0,-1]:    #L
            for x in range(180):
                rotateDegRight()
            direction = 4
            return
    elif direction == 4:
        if nextStep == [1,0]:       #F
            for x in range(90):
                rotateDegRight()
            direction = 1
            return
        elif nextStep == [0,1]:     #R
            for x in range(180):
                rotateDegRight()
            direction = 3
            return
        elif nextStep == [-1,0]:    #B
            for x in range(90):
                rotateDegLeft()
            direction = 2
            return
        elif nextStep == [0,-1]:    #L
            return