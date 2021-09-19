import numpy as np
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.distToCurPos = 0
        self.distToEndPos = 0
        self.cost = 0

    def __eq__(self, other):
        return self.position == other.position


def aStar(map, curPos, endPos):
    rootNode = Node(None, curPos)                        # beginning node
    rootNode.distToCurPos = 0
    sinkNode = Node(None, endPos)                        # ending node
    sinkNode.distToCurPos = sinkNode.distToEndPos = sinkNode.cost = 0
    rootNode.cost = rootNode.distToEndPos = (abs(rootNode.position[0] - sinkNode.position[0])) + (abs(rootNode.position[1] - sinkNode.position[1]))
    
    already_queued = False                                  # vars for astar traversal
    queue = []
    visited = []


    queue.append(rootNode)                               # add beginning node to queue

    while (len(queue) > 0):                                 # while nodes to process
        current_node = queue[0]                             # grab first index in queue
        current_index = 0

        for index, queued_node in enumerate(queue):         # traverse queue to find lowest cost node based on heuristic
            if (queued_node.cost < current_node.cost):      
                current_node = queued_node
                current_index = index
        queue.pop(current_index)                            # pop that node and add to visited  
        visited.append(current_node)

        if current_node == sinkNode:                     # if reached goal create path from reverse traversal
            path = []                                   
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]                               # reverse for return in proper orientation

        children = []
        for adjustment in [(0, -1), (0, 1), (-1, 0), (1, 0)]: 
            node_position = (current_node.position[0] + adjustment[0], current_node.position[1] + adjustment[1])
            if node_position[0] > (len(map) - 1) or node_position[0] < 0 or node_position[1] > (len(map[len(map)-1]) -1) or node_position[1] < 0:
                continue
            if map[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            child.distToCurPos = current_node.distToCurPos + 1
            child.distToEndPos = (abs(child.position[0] - sinkNode.position[0])) + (abs(child.position[1] - sinkNode.position[1]))
            child.cost = child.distToCurPos + child.distToEndPos
            for visited_node in visited:
                if child == visited_node and child.distToCurPos >= visited_node.distToCurPos:
                    already_queued = True
                    continue
            for queued_node in queue:
                if child == queued_node and child.distToCurPos >= queued_node.distToCurPos:
                    already_queued = True
                    continue
            if not already_queued:
                queue.append(child)
            already_queued = False
    
    
    current_node = visited[0]                   # we traversed our map and found no path to solution
    current_index = 0                           # so find the choose randomly between lowest distTo, or farthest away and travel there
    if np.random.rand() > .5:
        print("Closest to end")
        for visited_node in visited:
            if (visited_node.distToEndPos < current_node.distToEndPos): # find closest to end   
                    current_node = visited_node
                    current_index = index
    else:
        print("Farthest away")
        for visited_node in visited:
            if (visited_node.distToCurPos > current_node.distToCurPos): # find max dist away     
                    current_node = visited_node
                    current_index = index
   
    path = []                                   
    while current_node is not None:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]  

def relativeListPath(path, x_loc, y_loc):
    result = []
    for x in path:
        x = list(x)
        x[0] = x_loc - x[0]
        x[1] = x[1] - y_loc
        result.append(x)
    return result
    
def main():

    map =  [[0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 1, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    curPos = (5, 5)
    endPos = (0, 0)

    path = aStar(map, curPos, endPos)

    print(relativeListPath(path,5,5))

    for x in path:
        map[x[0]][x[1]]= 7

    print(map)

if __name__ == '__main__':
    main()