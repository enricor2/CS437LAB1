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

def RadarScan():
    results = []
    for i in range(360):
        rotateDegRight()
        dist = 50*ultra.checkdist() # each value is 2 cm
        if dist > 50:
            dist = 0
        results.append([int(dist*np.sin(x*np.pi/180)),int(dist*np.cos(x*np.pi/180))])
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
    print(num_rows,num_cols)
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
        grid[int(num_rows/2 - y_loc - y0 - 1)][int(num_cols/2 + x_loc + x0 - 1)] = 1
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
        grid = np.zeros(100,100)
        createMapping(0,0,grid)
        print(grid)
    except KeyboardInterrupt:
        move.destroy()