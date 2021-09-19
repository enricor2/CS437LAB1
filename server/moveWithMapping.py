import ultra
import move
import time
import numpy as np
import sys
import aStar
import rotation
move.setup()
np.set_printoptions(threshold=sys.maxsize)

if __name__ == '__main__':
    try:
        x_loc = 0
        y_loc = 0
        print("X position to travel to in m: ")
        x = int(float(input())/.02)
        if x >= 50:
            print("Max distance is 1 m")
            x = 49
        print("y position to travel to in m: ")
        y = int(float(input())/.02)
        if y >= 50:
            print("Max distance is 1 m")
            y = 49
        print("Please wait for rotation testing...")
        rotation.getRotationTime()
        print("Please wait for distance testing...")
        getTravelTime()
        
        while (x_loc != x or y_loc != y):
            print("Scanning surroundings")
            grid = np.full((100,100),0)
            num_rows, num_cols = grid.shape
            offset = int(num_rows/2-1)
            mapping.createMapping(0,0,grid)
            # grid =  np.asarray([[0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            #                     [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            #                     [0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
            #                     [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            #                     [0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
            #                     [1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            #                     [0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
            #                     [0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            #                     [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            #                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
            print(grid)
        
            print("Planning a path")
            path = aStar.relativeListPath(aStar.aStar(grid,(offset,offset),(offset-y,offset+x)),offset,offset)
            print(path)
            print("Following path...")
            x_loc, y_loc = mapping.followPath(path,x_loc,y_loc,path[-1]==[y,x])
            print("Path ended at",y_loc,x_loc," going to ", y, x)
    except KeyboardInterrupt:
        move.destroy()