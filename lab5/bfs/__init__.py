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
