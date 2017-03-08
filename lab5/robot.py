from grid import *
from dijkstra import *
import time
#from ekf import EKF
#from bfs import *


DELAY_SEC = 500

# control inputs
pwm1 = 0
pwm2 = 0
inputs = [pwm1, pwm2]
directions = ["+x", "-x", "+y", "-y"]
pos_start = (4, 3)
pos_finish = (10, 10)

# add barriers
barriers = [
    (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
    (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
    (7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
    (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
    (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)
]

class Robot(object):

    mapping = []
    direction = ""

    def __init__(self, n, m, pos_start, pos_finish):
        self.mapping = WeightedGrid(n, m)
        self.mapping.obstabcles = barriers
        self.pos_start = pos_start
        self.pos_finish = pos_finish
        self.pos = pos_start
        self.init_boundaries()
        self.set_start(pos_start)
        self.set_finish(pos_finish)
        self.path = []
        self.report_status()

    def set_start(self, pos):
        self.mapping.set_position(pos, START)
        return

    def set_finish(self, pos):
        self.mapping.set_position(pos, FINISH)
        return

    def set_current(self, pos):
        self.pos = pos
        self.mapping.set_position(pos, CURRENT)
        return

    def set_discovered(self, pos):
        self.mapping.set_position(pos, DISCOVERED)

    def init_boundaries(self):
        for barrier in barriers:
            self.mapping.add_obstacle(barriers)
        return

    def calculate_path(self):
        came_from, cost_so_far = dijkstra_search(self.mapping, self.pos_start, self.pos_finish)
        self.path = reconstruct_path(came_from, start=pos_start, goal=pos_finish)
        for pos in self.path:
            (x, y) = pos
            if pos != self.pos_start and pos != self.pos_finish:
                self.mapping.set_position(pos, PATH)
        self.report_status()

    def automate(self):
        for pos in self.path:
            time.sleep(0.5)
            self.set_discovered(self.pos)
            self.pos = pos
            self.set_current(pos)
            self.report_status()
            #self.mapping

            if pos == pos_finish:
                print("======= PATH FOUND =======")
                return True

        print("======= FAILED: PATH CANT BE FOUND =======")
        return False

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
        print("{} : {}".format("Current Position [x, y]", [self.pos[0], self.pos[1]]))
        print("{} : {}".format("Direction", self.direction))
        print("Map:")
        self.mapping.print_grid()
        print("\n")

Car = Robot(15, 15, pos_start, pos_finish)
Car.calculate_path()
Car.automate()
# Car.report_status()
#draw_grid(Car.mapping, path=reconstruct_path(came_from, start=pos_start, goal=pos_finish))
