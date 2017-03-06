from grid import Grid

DELAY_MSEC = 500

# control inputs
pwm1 = 0
pwm2 = 0
Input = [pwm1, pwm2]

Desk = Grid(10, 10)
Map = Desk.grid
Desk.add_obstacle(1, 2, 1)

print("{} : {}".format("Input", Input))
print("Map:")
print(Map)
