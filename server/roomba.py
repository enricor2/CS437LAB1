import ultra
import move
import time
import numpy as np
move.setup()

rotationTime = .0165

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

def roomba():
        if ultra.checkdist() < .5:
                move.move(70, 'backward', 'no', .5)
                time.sleep(.75)
                if np.random.rand() > .5:
                        for x in range(90):
                                rotateDegRight()
                                x+=1
                else:
                        for x in range(90):
                                rotateDegLeft()
                                x+=1
        else:
                move.move(50,'forward', 'no', .5)
        time.sleep(.05)


if __name__ == '__main__':
        try:
                getRotationTime()
                while(True):
                        roomba()
        except KeyboardInterrupt:
                move.destroy()