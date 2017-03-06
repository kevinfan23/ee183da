import random as rm

def gyro(w):
	w = w + rm.uniform(-0.024,0.024)*w
	return w

def wheel_velocity(v):
	v = v + rm.uniform(-0.045,0.045)*v
	return v

def PWM2left_velocity(PWM):
	v = ((90 - PWM)/90)*0.22
	print (v)
	return
def PWM2right_velocity(PWM):
	v = ((PWM - 90)/90)*0.22
	print (v)
	return
