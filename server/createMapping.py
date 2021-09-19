import ultra
import move
import time
import numpy as np
import sys
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('WXAgg')
move.setup()
np.set_printoptions(threshold=sys.maxsize)
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

def RadarScan():
    results = []
    for i in range(360):
        rotateDegRight()
        dist = 12.5*ultra.checkdist()   # each value is 8 cm (100 unit grid covers 4 m working distance of ultrasonic) display uses 20x20
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

if __name__ == '__main__':
    try:
        getRotationTime()
        grid = np.full((100,100),0)
        createMapping(0,0,grid)
        plt.title("Map of Objects")
        plt.imshow(grid,cmap='Greys_r')
        plt.show()
    except KeyboardInterrupt:
        move.destroy()