'''
    Extended Kalman Filter in Python
'''
import numpy as np
from numpy.linalg import inv
from math import *
import random as rm

DELAY_SEC = 0.5
L = 4.25
#r = 3

# set v_k: the control error
v_k = 0.02
V_MAX = 1/0.5 + v_k

class EKF(object):

    def __init__(self, x, y, n=6, m=3):
        self.num_states = n
        self.num_measurements = m
        self.S = np.array([x, y, 0, 0, 0, 0])
        self.U = np.array([0, 0])

    def step(self, u1, u2):
        #A Matrix
        self.U = np.array([u1,u2])
        P = np.eye(self.num_states)
        A = np.eye(self.num_states)
        A[3][3] = 0
        A[4][4] = 0
        A[5][5] = 0

        #B Matrix
        B = np.array([
        	[0.5*cos(self.S[2])*DELAY_SEC,0.5*cos(self.S[2])*DELAY_SEC],
        	[0.5*sin(self.S[2])*DELAY_SEC,0.5*sin(self.S[2])*DELAY_SEC],
        	[-1/(2*L)*DELAY_SEC,1/(2*L)*DELAY_SEC],
        	[0.5*cos(self.S[2]),0.5*cos(self.S[2])],
        	[0.5*sin(self.S[2]),0.5*sin(self.S[2])],
        	[-1/(2*L),1/(2*L)]])

        #predict
        self.S = np.dot(A,self.S)+np.dot(B,self.U)
        P = np.dot(np.dot(A,P),np.transpose(A))
        #print (x)
        if u1 == V_MAX and u2 == V_MAX:
        	z = np.array([u1+rm.uniform(-0.01,0.01),u2+rm.uniform(-0.01,0.01),0])
        	C = np.array([
        		[0,0,0,self.S[3]/(sqrt(self.S[3]**2+self.S[4]**2)),self.S[4]/(sqrt(self.S[3]**2+self.S[4]**2)),0],
        		[0,0,0,self.S[3]/(sqrt(self.S[3]**2+self.S[4]**2)),self.S[4]/(sqrt(self.S[3]**2+self.S[4]**2)),0],
        		[0,0,0,0,0,0]
        		])
        elif u1 == -V_MAX and u2 == -V_MAX:
        	z = np.array([-(u1+rm.uniform(-0.01,0.01)),-(u2+rm.uniform(-0.01,0.01)),0])
        	C = np.array([
        		[0,0,0,-self.S[3]/(sqrt(self.S[3]**2+self.S[4]**2)),-self.S[4]/(sqrt(self.S[3]**2+self.S[4]**2)),0],
        		[0,0,0,-self.S[3]/(sqrt(self.S[3]**2+self.S[4]**2)),-self.S[4]/(sqrt(self.S[3]**2+self.S[4]**2)),0],
        		[0,0,0,0,0,0]
        		])
        elif u1 == V_MAX and u2 == -V_MAX:
        	z = np.array([u1+rm.uniform(-0.01,0.01),-(u2+rm.uniform(-0.01,0.01)),0])
        	C = np.array([
        		[0,0,0,0,0,-L],
        		[0,0,0,0,0,-L],
        		[0,0,0,0,0,1]
        		])
        elif u1 == -V_MAX and u2 == V_MAX:
        	z = np.array([-(u1+rm.uniform(-0.01,0.01)),u2+rm.uniform(-0.01,0.01),0])
        	C = np.array([
        	[0,0,0,0,0,L],
        	[0,0,0,0,0,L],
        	[0,0,0,0,0,1]
        	])

        #Update states and covariances
        temp = np.dot(np.dot(C,P),np.transpose(C))
        temp2 = inv(temp + np.eye(self.num_measurements))
        G = np.dot(np.dot(P,np.transpose(C)),temp2)
        self.S = self.S + np.dot(G,(z-(np.dot(C,self.S))))
        P = (np.eye(self.num_states)-np.dot(G,C))

        return self.S
