
import numpy as np

OBSTACLE = -1
DISCOVERED = 1
CURRENT = 9

class Grid(object):

    def __init__(self, n, m):
        # Creates a matrix.
        self.grid = np.zeros((n,m))

    def add_obstacle(self, row, column):
        self.grid[row - 1][column - 1] = OBSTACLE
        return

    def mark_discovered(self. row, column)
        self.grid[row - 1][column - 1] = DISCOVERED
        return

    def set_current(self. row, column):
        self.grid[row - 1][column - 1] = CURRENT
        return


    def print_grid():
        return self.grid
