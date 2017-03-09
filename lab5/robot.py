from grid import *
from dijkstra import *
from ekf import EKF
import time
from math import *
#from bfs import *


DELAY_SEC = 0.5

# control inputs
pwm1 = 0
pwm2 = 0
inputs = [pwm1, pwm2]
directions = {
    "+x": "\u2192",
    "-x": "\u2190",
    "+y": "\u2191",
    "-y": "\u2193"
}

pos_start = (4, 3)
pos_finish = (10, 10)

# Robot geometry measurements
L = 4.25
r = 3

# set v_k: the control error
v_k = 0.02
V_MAX = 1/0.5 + v_k

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

    def __init__(self, n, m, pos_start, pos_finish, direction="+x"):
        self.mapping = WeightedGrid(n, m)
        self.mapping.obstabcles = barriers
        self.init_boundaries()

        self.num_rows = n
        self.num_cols = m

        self.direction = direction
        self.pos_start = pos_start
        self.pos_finish = pos_finish

        self.pos_abs = pos_start
        self.pos_abs = (self.num_rows - 1 - pos_start[0], pos_start[1])

        self.pos = pos_start
        self.set_start(pos_start)
        self.set_finish(pos_finish)
        self.path = []
        self.inputs = [0, 0]

        # declare an efk instance
        self.ekf = EKF(self.pos_abs[1], self.pos_abs[0], 6, 3)

        self.report_status()

    def set_start(self, pos):
        self.mapping.set_position(pos, START)
        return

    def set_finish(self, pos):
        self.mapping.set_position(pos, FINISH)
        return

    def set_current(self, pos):
        self.pos = pos
        self.mapping.set_position(pos, directions[self.direction])
        return

    def set_discovered(self, pos):
        self.mapping.set_position(pos, DISCOVERED)

    def init_boundaries(self):
        for barrier in barriers:
            self.mapping.add_obstacle(barriers)
        return

    def move_forward(self):
        self.inputs = [V_MAX, V_MAX]
        self.ekf.S = self.ekf.step(V_MAX, V_MAX)
        return

    def move_backward(self):
        self.inputs = [-V_MAX, -V_MAX]
        self.ekf.S = self.ekf.step(-V_MAX, -V_MAX)
        return

    def turn_left(self):
        self.inputs = [-V_MAX, V_MAX]
        for i in range(7):
             self.ekf.S = self.ekf.step(-V_MAX, V_MAX)
        return

    def turn_right(self):
        self.inputs = [V_MAX, -V_MAX]
        for i in range(7):
            self.ekf.S = self.ekf.step(V_MAX, -V_MAX)
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
            time.sleep(DELAY_SEC)
            self.set_discovered(self.pos)

            # if the robot is moving vertically
            if pos[0] == self.pos[0]:
                if (pos[1] - self.pos[1]) == 1:
                    if self.direction == "+y":
                        self.turn_right()
                    elif self.direction == "-y":
                        self.turn_left()
                    elif self.direction == "+x":
                        self.move_forward()
                    elif self.direction == "-x":
                        self.move_backward()

                    self.direction = "+x"
                elif (pos[1] - self.pos[1]) == -1:
                    if self.direction == "+y":
                        self.turn_left()
                    elif self.direction == "-y":
                        self.turn_right()
                    elif self.direction == "+x":
                        self.move_backward()
                    elif self.direction == "-x":
                        self.move_forward()

                    self.direction = "-x"
            elif pos[1] == self.pos[1]:
                if (pos[0] - self.pos[0]) == 1:
                    if self.direction == "+y":
                        self.move_backward()
                    elif self.direction == "-y":
                        self.move_forward()
                    elif self.direction == "+x":
                        self.turn_right()
                        self.move_forward()
                    elif self.direction == "-x":
                        self.turn_left()
                        self.move_forward()

                    self.direction = "-y"
                elif (pos[0] - self.pos[0]) == -1:
                    if self.direction == "+y":
                        self.move_forward()
                    elif self.direction == "-y":
                        self.move_backward()
                    elif self.direction == "+x":
                        self.turn_left()
                    elif self.direction == "-x":
                        self.turn_right()

                    self.direction = "+y"

            self.pos = pos
            self.pos_abs = (self.num_rows - 1 - pos[0], pos[1])
            self.set_current(pos)
            self.report_status()
            #self.mapping

            if pos == pos_finish:
                print("======= PATH FOUND =======\n")

                return True

        print("======= FAILED: PATH CANT BE FOUND =======\n")
        return False

    def report_status(self):
        print("{} : {}".format("Input", self.inputs))
        print("{} : {}".format("Current Position [x, y]", [self.pos_abs[1], self.pos_abs[0]]))
        print("{} : {}".format("Estimated States [x, y, theta, x_hat, y_hat, theta_hat]",
        [float(str.format('{0:.3f}', self.ekf.S[0])), float(str.format('{0:.3f}', self.ekf.S[1])), float(str.format('{0:.3f}', degrees(self.ekf.S[2]))), float(str.format('{0:.3f}', self.ekf.S[3])), float(str.format('{0:.3f}', self.ekf.S[4])), float(str.format('{0:.3f}', self.ekf.S[5])) ])
        )
        print("{} : {}".format("Direction", self.direction))
        print("Map:")
        self.mapping.print_grid()
        print("\n")

Car = Robot(15, 15, pos_start, pos_finish)

# z is the measurements, with dimension (m, 1), in this case (3, 1)
z = np.array([[1], [1], [1]])

Car.calculate_path()
Car.automate()
