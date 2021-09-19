import moveForward
import rotation
import move
import keyboard
move.setup()
if __name__ == '__main__':
    while(True):
        if keyboard.is_pressed('w'):
            moveForward.move1()
        elif keyboard.is_pressed('a'):
            rotation.rotateDegLeft()
        elif keyboard.is_pressed('d'):
            rotation.rotateDegRight()
    

