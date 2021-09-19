import ultra
import move
import time
import numpy as np
move.setup()

def rotateDegRight():
        move.move(100,'no','right',0.8)
        time.sleep(.0181)
        move.motorStop()
        time.sleep(.05)

def rotateDegLeft():
        move.move(100,'no','left',0.8)
        time.sleep(.01935)
        move.motorStop()
        time.sleep(.05)

def roomba():
        if ultra.checkdist() < .1:
                move.move(100, 'backward', 'no', .5)
                time.sleep(1.5)
                if np.random.rand() > .5:
                        for x in range(90):
                                rotateDegRight()
                                x+=1
                else:
                        for x in range(90):
                                rotateDegLeft()
                                x+=1
        else:
                move.move(100,'forward', 'no', .5)
        time.sleep(.1)


if __name__ == '__main__':
        try:
                while(True):
                        roomba()
        except KeyboardInterrupt:
                move.destroy()