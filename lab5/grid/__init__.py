
import numpy as np

EMPTY = "."
OBSTACLE = "#"
DISCOVERED = "o"
CURRENT = '@'

class Grid(object):
    num_rows = 0
    num_cols = 0
    grid = []

    def __init__(self, n, m):
        # Creates a matrix.
        self.num_rows = n
        self.num_cols = m
        self.grid = []

        for i in range(n):
            self.grid.append([])
            for j in range(m):
                self.grid[i].append(EMPTY)

    def add_obstacle(self, x, y):
        self.grid[x - 1][y - 1] = OBSTACLE
        return

    def set_discovered(self, x, y):
        self.grid[x - 1][y - 1] = DISCOVERED
        return

    def is_obstacle(self, x, y):
        if self.grid[x - 1][y - 1] == OBSTACLE:
            return True
        return False

    def set_current(self, x, y):
        self.grid[x - 1][y - 1] = CURRENT
        return

    def print_grid(self):
        for dot in self.grid:
            print(" ".join(map(str, dot)))
        return
        #print(self.grid)
