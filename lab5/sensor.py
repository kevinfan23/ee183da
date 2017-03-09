import numpy as np
from numpy.linalg import inv
from math import *
import random as rm

L = 4.25
y = np.array([0,0,0,0,0,0])
#z = np.array([0,0,0])
t = 0.5

# set v_k: the control error
v_k = 0.02
V_MAX = 1/0.5 + v_k

class EKF(object):


	def __init(self, n=6, m=3):
		self.num_states = n
		self.num_measurements = m
		self.S = np.array([0,0,0,0,0,0])


	def step(u1,u2,x):
		#A Matrix
		u = np.array([u1,u2])
		P = np.eye(6)
		A = np.eye(6)
		A[3][3] = 0
		A[4][4] = 0
		A[5][5] = 0

		#B Matrix
		B = np.array([
			[0.5*cos(x[2])*t,0.5*cos(x[2])*t],
			[0.5*sin(x[2])*t,0.5*sin(x[2])*t],
			[-1/(2*L)*t,1/(2*L)*t],
			[0.5*cos(x[2]),0.5*cos(x[2])],
			[0.5*sin(x[2]),0.5*sin(x[2])],
			[-1/(2*L),1/(2*L)]])

		#predict
		x = np.dot(A,x)+np.dot(B,u)
		P = np.dot(np.dot(A,P),np.transpose(A))
		#print (x)
		if u1 == V_MAX and u2 == V_MAX:
			z = np.array([u1+rm.uniform(-0.01,0.01),u2+rm.uniform(-0.01,0.01),0])
			C = np.array([
				[0,0,0,x[3]/(sqrt(x[3]**2+x[4]**2)),x[4]/(sqrt(x[3]**2+x[4]**2)),0],
				[0,0,0,x[3]/(sqrt(x[3]**2+x[4]**2)),x[4]/(sqrt(x[3]**2+x[4]**2)),0],
				[0,0,0,0,0,0]
				])
		elif u1 == -V_MAX and u2 == -V_MAX:
			z = np.array([-(u1+rm.uniform(-0.01,0.01)),-(u2+rm.uniform(-0.01,0.01)),0])
			C = np.array([
				[0,0,0,-x[3]/(sqrt(x[3]**2+x[4]**2)),-x[4]/(sqrt(x[3]**2+x[4]**2)),0],
				[0,0,0,-x[3]/(sqrt(x[3]**2+x[4]**2)),-x[4]/(sqrt(x[3]**2+x[4]**2)),0],
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

		#Update
		temp = np.dot(np.dot(C,P),np.transpose(C))
		temp2 = inv(temp + np.eye(3))
		G = np.dot(np.dot(P,np.transpose(C)),temp2)
		x = x + np.dot(G,(z-(np.dot(C,x))))
		P = (np.eye(6)-np.dot(G,C))

		print(x)
		return x

# 7*0.5 = 3.5s for turning left
# y = step(V_MAX,-V_MAX,y)
# y = step(V_MAX,-V_MAX,y)
# y = step(V_MAX,-V_MAX,y)
# y = step(V_MAX,-V_MAX,y)
# y = step(V_MAX,-V_MAX,y)
# y = step(V_MAX,-V_MAX,y)
# y = step(V_MAX,-V_MAX,y)

y = step(-V_MAX,-V_MAX,y)
y = step(-V_MAX,V_MAX,y)
y = step(-V_MAX,V_MAX,y)
y = step(-V_MAX,V_MAX,y)
y = step(-V_MAX,V_MAX,y)
y = step(-V_MAX,V_MAX,y)
y = step(-V_MAX,V_MAX,y)

# y = step(V_MAX,V_MAX,y)
# y = step(V_MAX,-V_MAX,y)
print(y)

# B = np.array(
# 	[0,0],
# 	[0,0],

# 	)
