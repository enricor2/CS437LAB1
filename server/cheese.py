import moveForward
import rotation
import move
import keyboard
if __name__ == '__main__':
    if keyboard.is_pressed('w'):
        moveForward.move1()
    elif keyboard.is_pressed('a'):
        rotation.rotateDegLeft()
    elif keyboard.is_pressed('d'):
        rotation.rotateDegRight()
    

