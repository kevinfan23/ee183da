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