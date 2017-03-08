import collections
import time

EMPTY = "."
OBSTACLE = "#"
DISCOVERED = "@"
CURRENT = "X"

START = "A"
FINISH = "B"

def BFS(pos_start, pos_finish, robot):
    #create an empty queue
    queue = collections.deque([pos_start])
    grid = robot.mapping
    #print(grid.neighbors(pos_start))

    while len(queue) > 0:
        time.sleep(0.5)
        node = queue.popleft()
        (x, y) = node
        if grid.is_not_discovered(node):
            robot.set_current(x, y)
            robot.report_status()
        else:
            continue

        next_level = list(filter(grid.is_not_discovered, grid.neighbors(node)))
        for i in range(len(next_level)):
            queue.append(next_level[i])

        if node == pos_finish:
            print("======= PATH FOUND =======")
            return

        if grid.is_passable(node) and grid.is_in_bounds(node):
            grid.set_discovered(node)
            continue

    print("======= FAILED: PATH CANT BE FOUND =======")
    return




# def BFS(x, y, grid):
#     #create an empty queue
#     queue = collections.deque([(x, y, None)])
#
#     while len(queue) > 0:
#         node = queue.popleft()
#
#         x = node[0] #get x and y
#         y = node[1]
#         if grid[x][y] == FINISH: #check if it's an exit
#             return GetPathFromNodes(node) #if it is then return the path
#         if (grid[x][y] != OBSTACLE or ): #if it's not a path, we can't try this spot
#             continue
#         grid[x][y] = DISCOVERED #make this spot explored so we don't try again
#         for i in [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]: #new spots to try
#             queue.append((i[0],i[1],node))#create the new spot, with node as the parent
#     return []
#
# def GetPathFromNodes(node):
#     path = []
#     while(node != None):
#         path.append((node[0],node[1]))
#         node = node[2]
#     return path
