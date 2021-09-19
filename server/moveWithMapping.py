import ultra
import move
import time
import numpy as np
import sys
import aStar
move.setup()
np.set_printoptions(threshold=sys.maxsize)
rotationTime = .0165
travelTime = .25
dir = 1 # 1-U 2-D 3-R 4-L

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

def getTravelTime():
    global travelTime
    move.move(50,'forward','no',0.8)
    time.sleep(travelTime)
    move.motorStop()
    print("Enter cms traveled forward: ")
    dist = float(input())
    travelTime = travelTime * 2 / dist
    if dist > 2:
        for x in range(int(dist/2)-1):
            move.move(50,'backward','no',0.8)
            time.sleep(travelTime)
    else:
        move.move(50,'backward','no',0.8)
        time.sleep(travelTime)
    move.motorStop()

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

def RadarScan():
    results = []
    for i in range(360):
        rotateDegRight()
        dist = 12.5*ultra.checkdist()   # each value is 8 cm (100 unit grid covers 4 m working distance of ultrasonic)
        if dist > 50:                   # still within the bounds of the array 
            dist = 0
        results.append([int(dist*np.sin(i*np.pi/180)),int(dist*np.cos(i*np.pi/180))])
    return results

def createMapping(x_loc,y_loc,map):
    points = RadarScan()
    prev = points[0]
    for point in points[1:]:
        if point[0] == 0 and point[1] == 0:
            prev = None
        elif prev == None:
            prev = point
        else:
            plotLine(prev[0],prev[1],point[0],point[1],map,x_loc,y_loc)
            prev = point

def plotLine(x0, y0, x1, y1,grid,x_loc,y_loc):
    num_rows, num_cols = grid.shape
    grid[int(num_cols/2-1)][int(num_rows/2-1)] = 9
    dx = abs(x1-x0)
    if x0<x1:
        sx = 1
    else:
        sx = -1
    dy = -abs(y1-y0)
    if y0<y1:
        sy = 1
    else:
        sy = -1
    err = dx+dy
    while (True):
        try:
            grid[int(num_rows/2 - y_loc - y0 - 1)][int(num_cols/2 - x_loc - x0 - 1)] = 1
        except IndexError:
            print("The following point is out of the array bounds... (",x0,",",y0,")")
        if (x0 == x1 and y0 == y1):
            break
        e2 = 2*err
        if (e2 >= dy):
            err += dy
            x0 += sx
        if (e2 <= dx):
            err += dx
            y0 += sy 

def move2():
    global travelTime
    move.move(50,'forward','no',0.8)
    time.sleep(travelTime)
    move.motorStop()

def followPath(path,x_loc, y_loc, dir,numStep = 400):
    for x in range (numStep):
        if path[x] == path[-1]:
            print("Arrived at end of path.")
            return x_loc, y_loc
        nextStep = path[x+1]-path[x]    
        turn(dir,nextStep)
        for x in range(4):
            move2()

def turn(dir, nextStep):
    if dir == 1:                    #F
        if nextStep == [1,0]:       #F
            return
        elif nextStep == [0,1]:     #R
            for x in range(90):
                rotateDegRight()
            dir = 3
            return
        elif nextStep == [-1,0]:    #B
            for x in range(180):
                rotateDegRight()
            dir = 2
            return
        elif nextStep == [0,-1]:    #L
            for x in range(90):
                rotateDegLeft()
            dir = 4
            return
    elif dir == 2:                  #B
        if nextStep == [1,0]:       #F
            for x in range(180):
                rotateDegRight()
            dir = 1
            return
        elif nextStep == [0,1]:     #R
            for x in range(90):
                rotateDegLeft()
            dir = 3
            return
        elif nextStep == [-1,0]:    #B
            return
        elif nextStep == [0,-1]:    #L
            for x in range(90):
                rotateDegRight()
            dir = 4
            return
    elif dir == 3:                  #R
        if nextStep == [1,0]:       #F
            for x in range(90):
                rotateDegLeft()
            dir = 1
            return
        elif nextStep == [0,1]:     #R
            return
        elif nextStep == [-1,0]:    #B
            for x in range(90):
                rotateDegRight()
            dir = 2
            return
        elif nextStep == [0,-1]:    #L
            for x in range(180):
                rotateDegRight()
            dir = 4
            return
    elif dir == 4:
        if nextStep == [1,0]:       #F
            for x in range(90):
                rotateDegRight()
            dir = 1
            return
        elif nextStep == [0,1]:     #R
            for x in range(180):
                rotateDegRight()
            dir = 3
            return
        elif nextStep == [-1,0]:    #B
            for x in range(90):
                rotateDegLeft()
            dir = 2
            return
        elif nextStep == [0,-1]:    #L
            return



if __name__ == '__main__':
    try:
        x_loc = 0
        y_loc = 0
        print("X position to travel to in m: ")
        x = int(float(input())/.08)
        print("y position to travel to in m: ")
        y = int(float(input())/.08)
        print("Please wait for rotation testing...")
        getRotationTime()
        print("Please wait for distance testing...")
        getTravelTime()
        
        print("Scanning surroundings")
        grid = np.full((100,100),0)
        createMapping(0,0,grid)
        print("Planning a path")
        path = aStar.relativeListPath(aStar.aStar(grid,(49,49),(49-x,y-49)),49,49)
        while (x_loc != x and y_loc != y):
            if path[-1] != (x,y):
                x_loc, y_loc = followPath(path,x_loc,dir,6)
            else:
                x_loc,y_loc = followPath(path,x_loc,dir)

        print(path)
        print("Beginning travel...")
        
    
    except KeyboardInterrupt:
        move.destroy()