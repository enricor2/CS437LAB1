import ultra
import move
import time
import numpy as np
import rotation
move.setup()


def roomba():
        if ultra.checkdist() < .15:
                move.move(50, 'backward', 'no', .5)
                time.sleep(.75)
                move.motorStop()
                if np.random.rand() > .5:
                        for x in range(90):
                                rotation.rotateDegRight()
                                x+=1
                else:
                        for x in range(90):
                                rotateDegLeft()
                                x+=1
        else:
                move.move(40,'forward', 'no', .5)
                time.sleep(.05)

# def roomba_pass_obj():


if __name__ == '__main__':
        try:
                rotation.getRotationTime()
                while(True):
                        roomba()
        except KeyboardInterrupt:
                move.destroy()