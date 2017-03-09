from grid import *
from dijkstra import *
from ekf import kalman
import time
from math import *
#from bfs import *


DELAY_SEC = 0.5

# control inputs
pwm1 = 0
pwm2 = 0
inputs = [pwm1, pwm2]
directions = ["+x", "-x", "+y", "-y"]
pos_start = (4, 3)
pos_finish = (10, 10)

# Robot geometry measurements
L = 4.25
r = 3
vmax = 0.22

# add barriers
barriers = [
    (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
    (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
    (7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
    (8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
    (9, 4), (9, 5), (9, 6), (9, 7), (9, 8)
]

class RobotEKF(EKF):
    '''
    An EKF for mouse tracking
    '''

    def __init__(self, n, m, x, y, theta=0):

        # Four states, two measurements (X,Y)
        EKF.__init__(self, n, m)

        self.x[0] = x
        self.x[1] = y
        self.x[2] = theta
        self.num_states = n
        self.num_measurements = m


    def f(self, x):
        F = np.array([
           [self.x[0] + self.x[3]*DELAY_SEC],
           [self.x[1] + self.x[4]*DELAY_SEC],
           [self.x[2] + self.x[5]*DELAY_SEC],
           [pwm1*(-1/2)*cos(self.x[2])*vmax/90 + pwm2*(1/2)*cos(self.x[2])*vmax/90],
           [pwm1*(-1/2)*sin(self.x[2])*vmax/90 + pwm2*(1/2)*sin(self.x[2])*vmax/90],
           [pwm1*vmax/(180*L) - pwm2*vmax/(180*L)]
        ])
        # State-transition function is identity
        return F

    def getF(self, x):
        A = np.eye(6)
        A[0][0] = 1;
        A[0][3] = DELAY_SEC;
        A[1][1] = 1;
        A[1][4] = DELAY_SEC;
        A[2][2] = 1;
        A[2][5] = DELAY_SEC;

        # So state-transition Jacobian is identity matrix
        return A

    def h(self, x):
        H = np.array([
            [self.x[3]*cos(self.x[2]) + self.x[4]*sin(self.x[2]) + self.x[5]*(L/2)],
            [self.x[3]*cos(self.x[2]) + self.x[4]*sin(self.x[2]) - self.x[5]*(L/2)]
            [self.x[2]]
        ])

        # Observation function is identity
        return H

    def getH(self, x):
        # C = np.array()
        # C[0][3] = cos(self.x[2]);
        # C[0][4] = sin(self.x[2]) ;
        # C[0][5] = L/2 ;
        # C[1][3] = cos(self.x[2]);
        # C[1][4] = sin(self.x[2]);
        # C[1][5] = L/2 ;
        # C[2][5] = 1;

        C = np.array([
            [0, 0, 0, cos(self.x[2]), sin(self.x[2]), L/2],
            [0, 0, 0, cos(self.x[2]), sin(self.x[2]), L/2],
            [0, 0, 0, 0, 0, 1],
        ])

        print(C)

        # So observation Jacobian is identity matrix
        return C

    def report_states(self):
        print("{} {}".format("Predicted States [x, y, theta, x_hat, y_hat, theta_hat] \n", self.x))
        print("\n")
        return

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

        # declare an efk instance
        self.ekf = RobotEKF(6, 3, pos_start[0], pos_start[1])

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
            time.sleep(DELAY_SEC)
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

    def report_status(self):
        print("{} : {}".format("Input", inputs))
        print("{} : {}".format("Current Position [x, y]", [self.pos[0], self.pos[1]]))
        self.ekf.report_states()
        #print("{} : {}".format("Direction", self.direction))
        print("Map:")
        self.mapping.print_grid()
        print("\n")

Car = Robot(15, 15, pos_start, pos_finish)
Car.ekf.step((1, 1, 1))

# Car.calculate_path()
# Car.automate()
