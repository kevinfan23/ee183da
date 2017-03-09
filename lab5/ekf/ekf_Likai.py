import cv2
import numpy as np
from sys import exit

from tinyekf import EKF

class TrackerEKF(EKF):
    '''
    An EKF for mouse tracking
    '''
L = 4.25
r = 3
theta = 0
t = 0.05
vmax = 0.22

def __init__(self):

    EKF.__init__(self, 6, 3)

def f(self, x):

    # State-transition function is identity
    return np.array[
       [this->x[0] + this->x[3]*t],
       [this->x[1] + this->x[4]*t],
       [this->x[2] + this->x[5]*t],
       [u1*(-1/2)*cos(theta)*vmax/90 + u2*(1/2)*cos(theta)*vmax/90],
       [u1*(-1/2)*sin(theta)*vmax/90 + u2*(1/2)*sin(theta)*vmax/90],
       [u1*vmax/(180*L) - u2*vmax/(180*L)]]

def getF(self, x):

    # So state-transition Jacobian is identity matrix
    return np.array[
       [1,0,0,t,0,0],
       [0,1,0,0,t,0],
       [0,0,1,0,0,t],
       [0,0,0,0,0,0],
       [0,0,0,0,0,0],
       [0,0,0,0,0,0]]

def h(self, x):
    C =
    return np.array[
    [this->x[3]*cos(theta) + this->x[4]*sin(theta) + this->x[5]*(L/2)],
    [this->x[3]*cos(theta) + this->x[4]*sin(theta) - this->x[5]*(L/2)]
    [this->x[2]]]
    # Observation function is identity

def getH(self, x):

    # So observation Jacobian is identity matrix
    return np.array[
       [0,0,cos(theta),sin(theta),L/2,0],
       [0,0,cos(theta),sin(theta),L/2,1],
       [0,0,0,0,0,0]]
