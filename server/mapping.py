import rotation
import time
import numpy as np
import ultra
import moveForward

def RadarScan():
    results = []
    for i in range(360):
        rotation.rotateDegRight()
        dist = 100*ultra.checkdist()  # each value is 1 cm 
        if dist == -2:
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
            plotLineWithPadding(prev[0],prev[1],point[0],point[1],map,x_loc,y_loc)
            prev = point

# simple line plotting algo that works for +- and slopes <1 >1
def plotLine(x0, y0, x1, y1,grid,x_loc,y_loc):
    num_rows, num_cols = grid.shape
    grid[int(num_cols/2-1)][int(num_rows/2-1)] = 0
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


def plotLineWithPadding(x0, y0, x1, y1,grid,x_loc,y_loc):
    plotLine(x0, y0, x1, y1,grid,x_loc,y_loc)
    plotLine(x0, y0+1, x1, y1+1,grid,x_loc,y_loc)
    plotLine(x0, y0-1, x1, y1-1,grid,x_loc,y_loc)
    plotLine(x0-1, y0, x1-1, y1,grid,x_loc,y_loc)
    plotLine(x0+1, y0, x1+1, y1,grid,x_loc,y_loc)

def followPath(path,x_loc, y_loc,endReached):
    global direction
    if endReached:
        numStep = len(path) - 1
    else: 
        numStep = 5
    for x in range (numStep):
        if (ultrasonic.checkdist < .08):
            Print("Rescanning, encountered new obstacle...")
            return
        if path[x] == path[-1]:
            print("Arrived at end of path.")
            return x_loc, y_loc
        nextStep = [path[x+1][0]-path[x][0],path[x+1][1]-path[x][1]]    
        rotation.turn(nextStep)
        y_loc += nextStep[0]
        x_loc += nextStep[1]
        print("move1",nextStep, direction)
        moveForward.move1()
    return x_loc,y_loc