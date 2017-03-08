from grid import Grid
#from ekf import EKF
from bfs import *


DELAY_SEC = 500

START = "A"
FINISH = "B"

# control inputs
pwm1 = 0
pwm2 = 0
inputs = [pwm1, pwm2]
directions = ["+x", "-x", "+y", "-y"]
pos_start = (3, 3)
pos_finish = (10, 6)

# add barriers
barriers = [
    (5, 3), (5, 4), (5, 5), (5, 6), (5, 7),
    (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
    (7, 6), (7, 7), (7, 8), (7, 8), (7, 10),
    (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
    (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)
]

class Robot(object):

    mapping = []
    direction = ""
    x = 0
    y = 0

    def __init__(self, n, m, x, y, direction="+x"):
        self.mapping = Grid(n, m)
        self.mapping.obstabcles = barriers
        self.direction = direction
        self.x = x
        self.y = y
        self.init_boundaries()
        self.set_start(x, y)
        self.set_finish(x, y)
        self.report_status()

    def set_start(self, x, y):
        self.x = x
        self.y = y
        self.mapping.set_position(x, y, START)
        return

    def set_finish(self, x, y):
        self.mapping.set_position(pos_finish[0], pos_finish[1], FINISH)
        return

    def set_current(self, x, y):
        self.x = x
        self.y = y
        self.mapping.set_position(x, y, CURRENT)
        return

    def init_boundaries(self):
        for barrier in barriers:
            self.mapping.add_obstacle(barrier[0], barrier[1])
        return

    def move_forward(self):
        if self.direction == "+x":
            if self.mapping.is_obstacle(self.x+1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x+1, self.y)
                # self.x = self.x + 1
                self.report_status()
                return True
        elif self.direction == "+y":
            if self.mapping.is_obstacle(self.x, self.y+1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x, self.y+1)
                # self.y = self.y + 1
                self.report_status()
                return True
        elif self.direction == "-x":
            if self.mapping.is_obstacle(self.x-1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x-1, self.y)
                # self.x = self.x - 1
                self.report_status()
                return True
        elif self.direction == "-y":
            if self.mapping.is_obstacle(self.x, self.y-1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x, self.y-1)
                # self.y = self.y - 1
                self.report_status()
                return True
        else:
            self.report_status()
            return False

    def move_back(self):
        if self.direction == "+x":
            if self.mapping.is_obstacle(self.x-1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x-1, self.y)
                # self.x = self.x - 1
                self.report_status()
                return True
        elif self.direction == "+y":
            if self.mapping.is_obstacle(self.x, self.y-1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x, self.y-1)
                # self.y = self.y - 1
                self.report_status()
                return True
        elif self.direction == "-x":
            if self.mapping.is_obstacle(self.x+1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x+1, self.y)
                # self.x = self.x + 1
                self.report_status()
                return True
        elif self.direction == "-y":
            if self.mapping.is_obstacle(self.x, self.y+1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_current(self.x, self.y+1)
                # self.y = self.y + 1
                self.report_status()
                return True
        else:
            self.report_status()
            return False

    def turn_left(self):
        if self.direction == "+x":
            self.direction = "+y"
            self.report_status()
            return True
        elif self.direction == "+y":
            self.direction = "-x"
            self.report_status()
            return True
        elif self.direction == "-x":
            self.direction = "-y"
            self.report_status()
            return True
        elif self.direction == "-y":
            self.direction = "+x"
            self.report_status()
            return True
        else:
            self.report_status()
            return False

    def turn_right(self):
        if self.direction == "+x":
            self.direction = "-y"
            self.report_status()
            return True
        elif self.direction == "+y":
            self.direction = "+x"
            self.report_status()
            return True
        elif self.direction == "-x":
            self.direction = "+y"
            self.report_status()
            return True
        elif self.direction == "-y":
            self.direction = "-x"
            self.report_status()
            return True
        else:
            self.report_status()
            return False

    def report_status(self):
        print("{} : {}".format("Input", inputs))
        print("{} : {}".format("Position [x, y]: ", [self.x, self.y]))
        print("{} : {}".format("Direction", self.direction))
        print("Map:")
        self.mapping.print_grid()
        print("\n")

Car = Robot(11, 11, pos_start[0], pos_start[1])
BFS(pos_start, pos_finish, Car)
