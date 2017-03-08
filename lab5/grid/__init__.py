
import numpy as np

EMPTY = "."
OBSTACLE = "#"
DISCOVERED = "o"
PATH = "@"
CURRENT = "X"

START = "A"
FINISH = "B"

# class Grid(object):
#     num_rows = 0
#     num_cols = 0
#     grid = []
#
#     def __init__(self, n, m):
#         # Creates a matrix.
#         self.num_rows = n
#         self.num_cols = m
#         self.grid = []
#         self.obstabcles = []
#
#         for i in range(n):
#             self.grid.append([])
#             for j in range(m):
#                 self.grid[i].append(EMPTY)
#
#     def add_obstacle(self, x, y):
#         self.grid[x][y] = OBSTACLE
#         return
#
#
#     def is_discovered(self, pos):
#         (x, y) = pos
#         return self.grid[x][y] == DISCOVERED
#
#     def is_in_bounds(self, pos):
#         (x, y) = pos
#         return 0 <= x < self.num_cols and 0 <= y < self.num_rows
#
#     def is_passable(self, pos):
#         return pos not in self.obstabcles
#
#     def is_not_discovered(self, pos):
#         (x, y) = pos
#         return self.grid[x][y] != DISCOVERED
#
#     def neighbors(self, pos):
#         (x, y) = pos
#         results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
#         #if (x + y) % 2 == 0: results.reverse() # aesthetics
#         results = list(filter(self.is_in_bounds, results))
#         results = list(filter(self.is_passable, results))
#         return results
#
#     def get_grid_status(self, pos):
#         return grid[pos[0], pos[1]]
#
#     def set_position(self, x, y, symbol):
#         self.grid[x][y] = symbol
#         return
#
#     def print_grid(self):
#         for dot in self.grid:
#             print(" ".join(map(str, dot)))
#         return
#         #print(self.grid)

def draw_tile(graph, pos, style, width):
    r = "."
    if 'number' in style and pos in style['number']: r = "%d" % style['number'][id]
    if 'start' in style and pos == style['start']: r = START
    if 'goal' in style and pos == style['goal']: r = FINISH
    if 'path' in style and pos in style['path']: r = "@"
    if pos in graph.obstabcles: r = "#"
    return r

def draw_grid(graph, width=2, **style):
    for i in range(graph.num_rows):
        for j in range(graph.num_cols):
            print("%%-%ds" % width % draw_tile(graph, (i, j), style, width), end="")
        print()

class Grid(object):
    def __init__(self, n, m):
        # Creates a matrix.
        self.num_rows = n
        self.num_cols = m
        self.grid = []
        self.obstabcles = []

        for i in range(n):
            self.grid.append([])
            for j in range(m):
                self.grid[i].append(EMPTY)

    def set_position(self, pos, symbol):
        self.grid[pos[0]][pos[1]] = symbol
        return

    def add_obstacle(self, barriers):
        self.obstabcles = barriers
        for pos in self.obstabcles:
            self.grid[pos[0]][pos[1]] = OBSTACLE
        return

    def is_in_bounds(self, pos):
        (x, y) = pos
        return 0 <= x < self.num_rows and 0 <= y < self.num_cols

    def is_passable(self, pos):
        return pos not in self.obstabcles

    def neighbors(self, pos):
        (x, y) = pos
        next_level = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        #if (x + y) % 2 == 0: next_level.reverse()
        next_level = filter(self.is_in_bounds, next_level)
        next_level = filter(self.is_passable, next_level)
        return next_level

    def print_grid(self):
        for dot in self.grid:
            print(" ".join(map(str, dot)))
        return

class WeightedGrid(Grid):
    def __init__(self, n, m):
        super().__init__(n, m)
        self.weights = {}

    def cost(self, node_from, node_to):
        return self.weights.get(node_to, 1)
