#!/usr/bin/python/

import numpy as np
from math import *
from pprint import pprint
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


identityMatrix_44 = np.matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])

max_thetaX = 90
min_thetaX = -90
max_thetaY = 90
min_thetaY = -90
max_thetaZ = 90
min_thetaZ = -90
max_thetaA = 45
min_thetaA = -45
default_thetaA = 45

interval_level1 = 10
interval_level2 = 4
interval_level3 = 2
interval_level4 = 1

# class of transformation matrix
# forward kinematic class
# inverse kinematic class
# class of a transformation matrix

# the end effector class
class EndEffector(object):
    def __init__(self):
        self.px = 0
        self.py = 0
        self.pz = 0
        self.pos = np.matrix([[self.px], [self.py], [self.pz], [1]])

    def setPos(self, x, y, z):
        self.px = x
        self.py = y
        self.pz = z
        self.pos = np.matrix([[self.px], [self.py], [self.pz], [1]])


# the Forward Kinematics class
class FK(object):
    def __init__(self):
        self.transMatrix = identityMatrix_44
        self.endEffector = EndEffector()

    def setEndEffector(self, x, y, z):
        self.endEffector.setPos(x, y, z)

    def addTransMatrix(self, type, a, p):
        a = radians(a)

        if type == "rx":
            added = np.matrix([
                [1, 0, 0, p[0]],
                [0, cos(a), -sin(a), p[1]],
                [0, sin(a), cos(a), p[2]],
                [0, 0, 0, 1]
            ])

        elif type == "ry":
            added = np.matrix([
                [cos(a), 0, sin(a), p[0]],
                [0, 1, 0, p[1]],
                [-sin(a), 0, cos(a), p[2]],
                [0, 0, 0, 1]
            ])

        elif type == "rz":
            added = np.matrix([
                [cos(a), -sin(a), 0, p[0]],
                [sin(a), cos(a), 0, p[1]],
                [0, 0, 1, p[2]],
                [0, 0, 0, 1]
            ])

        else:
            added = identityMatrix_44

        self.transMatrix = added * self.transMatrix
        #print self.transMatrix

    def calculateFK(self):
        return self.transMatrix * self.endEffector.pos

""" set default position of the robot, in its operational space,
let thetaX = 0, thetaY = 0, thetaZ = 0, thetaA = 45, calculate its coordinates in the
base frame.
"""
human_arm = FK()
human_arm.setEndEffector(0, 0, 0)
human_arm.addTransMatrix("rx", 0, [0.25, 0, 0])
human_arm.addTransMatrix("rz", default_thetaA, [0.2, 0, 0])
human_arm.addTransMatrix("rx", 90, [0, 0, 0])
human_arm.addTransMatrix("rz", 90, [0, 0, 0])
human_arm.addTransMatrix("rx", 90, [0, 0, 0])

# print human_arm.calculateFK()

lookUpTable = dict()

""" function for simulate every position of the robotic linkage
we use Python dictionary to store all possible configurations of the joints according to
every point in the operational space
"""

def simulateIK():

    for tx in np.arange(min_thetaX, max_thetaX + interval_level1, interval_level1):
        for ty in np.arange(min_thetaY, max_thetaY + interval_level1, interval_level1):
            for tz in np.arange(min_thetaZ, max_thetaZ + interval_level1, interval_level1):
                for ta in np.arange(min_thetaA, max_thetaA + interval_level1, interval_level1):
                    robot = FK()
                    robot.setEndEffector(0, 0, 0)
                    robot.addTransMatrix("rx", 0, [0.25, 0, 0])
                    robot.addTransMatrix("rz", default_thetaA, [0.2, 0, 0])
                    robot.addTransMatrix("rx", 90, [0, 0, 0])
                    robot.addTransMatrix("rz", 90, [0, 0, 0])
                    robot.addTransMatrix("rx", 90, [0, 0, 0])

                    robot.addTransMatrix("rx", tx, [0, 0, 0])
                    robot.addTransMatrix("ry", ty, [0, 0, 0])
                    robot.addTransMatrix("rz", tz, [0, 0, 0])
                    robot.addTransMatrix("rz", ta, [0, 0, 0])


                    loopUpKey = robot.calculateFK().tolist()

                    # convert all float to integers
                    for i in range(0, 3):
                        loopUpKey[i][0] = round(loopUpKey[i][0], 2)

                    lookUpTable[str(loopUpKey)] = [tx, ty, tz, ta]

    return lookUpTable

# [[0.0], [0.04], [0.41], [1.0]]': [-30, 0, 40, -45],
# lookUpKey = [[0.03], [-0.03], [0.41], [1.0]]
# posIK = simulateIK()
# pprint(posIK)

# forward kinematics trajectory
pos0 = human_arm.calculateFK().tolist()
print pos0

human_arm.addTransMatrix("rx", -30, [0, 0, 0])
pos1 = human_arm.calculateFK().tolist()
print pos1

human_arm.addTransMatrix("ry", 0, [0, 0, 0])
pos2 = human_arm.calculateFK().tolist()
print pos2

human_arm.addTransMatrix("rz", 40, [0, 0, 0])
pos3 = human_arm.calculateFK().tolist()
print pos3

human_arm.addTransMatrix("rz", -45, [0, 0, 0])
pos4 = human_arm.calculateFK().tolist()
print pos4

# generate forward kinematics trajectory plots
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [pos0[0], pos1[0], pos3[0], pos4[0]]
y = [pos0[1], pos1[1], pos3[1], pos4[1]]
z = [pos0[2], pos1[2], pos3[2], pos4[2]]
xs = [pos0[0], pos4[0]]
ys = [pos0[1], pos4[1]]
zs = [pos0[2], pos4[2]]

ax.scatter(x, y, z, c="b", marker="o")
ax.scatter(xs, ys, zs, c="r", marker="^")

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

fig.savefig('data.png')
