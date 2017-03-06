'''
A Python 3 Extended Kalman Filter implementation, modified from TinyEKF by Simon D. Levy
https://github.com/simondlevy/TinyEKF

'''
from numpy import matrix
import math

L = 4.25
r = 3
theta = 0
t = 0.5
vmax =0.22

A = matrix([1,0,0,t,0,0],[0,1,0,0,t,0],[0,0,1,0,0,t],[0,0,0,0,0,0]
	,[0,0,0,0,0,0],[0,0,0,0,0,0])
B = matrix([0,0],[0,0],[0,0],[-0.5*math.cos(0.0174*theta)*vmax/90,
	0.5*math.cos(0.0174*theta)*vmax/90],[-0.5*math.sin(0.0174*theta)*vmax/90,
	0.5*math.sin(0.0174*theta)*vmax/90],[vmax/180,-vmax/180])

class EKF(object):

	    def __init__(self, n, m, pval, qval, rval):
        '''
        Creates a KF object with n states, m observables, and specified values for
        prediction noise covariance pval, process noise covariance qval, and
        measurement noise covariance rval.
        '''

		# No previous prediction noise covariance
        self.P_pre = None

        # Current state is zero, with diagonal noise covariance matrix
        self.x = np.zeros((n,1))
        self.P_post = np.eye(n) * pval

        # Get state transition and measurement Jacobians from implementing class
        self.F = self.getF(self.x)
        self.C = self.getC(self.x)

        # Set up covariance matrices for process noise and measurement noise
        self.Q = np.eye(n) * qval
        self.R = np.eye(m) * rval

        # Identity matrix will be usefel later
        self.I = np.eye(n)
