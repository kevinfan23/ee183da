
import numpy as np

class Grid(object):

    def __init__(self, n, m):
        # Creates a matrix.
        self.grid = np.zeros((n,m))

    def add_obstacle(self, row, column, value):
        self.grid[row - 1][column - 1] = value
        return

    def print_grid():
        return self.grid
