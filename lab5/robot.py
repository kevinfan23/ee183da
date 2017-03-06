from grid import Grid

DELAY_SEC = 500

# control inputs
pwm1 = 0
pwm2 = 0
inputs = [pwm1, pwm2]
directions = ["+x", "-x", "+y", "-y"]

class Robot(object):

    mapping = []
    direction = ""
    x = 0
    y = 0

    def __init__(self, n, m, x, y, direction="+x"):
        self.mapping = Grid(n, m)
        self.direction = direction
        self.mapping.set_current(x, y)
        self.x = x
        self.y = y
        self.init_boundaries()
        self.report_status()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.mapping.set_current(x, y)
        return

    def init_boundaries(self):
        n = self.mapping.num_rows
        m = self.mapping.num_cols

        for i in range(n):
            self.mapping.add_obstacle(i, 1)
            self.mapping.add_obstacle(i, m)

        for j in range(m):
            self.mapping.add_obstacle(1, j)
            self.mapping.add_obstacle(n, j)

        return

    def move_forward(self):
        if self.direction == "+x":
            if self.mapping.is_obstacle(self.x+1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x+1, self.y)
                # self.x = self.x + 1
                self.report_status()
                return True
        elif self.direction == "+y":
            if self.mapping.is_obstacle(self.x, self.y+1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x, self.y+1)
                # self.y = self.y + 1
                self.report_status()
                return True
        elif self.direction == "-x":
            if self.mapping.is_obstacle(self.x-1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x-1, self.y)
                # self.x = self.x - 1
                self.report_status()
                return True
        elif self.direction == "-y":
            if self.mapping.is_obstacle(self.x, self.y-1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x, self.y-1)
                # self.y = self.y - 1
                self.report_status()
                return True
        else:
            self.report_status()
            return False

    def move_back(self):
        if self.direction == "+x":
            if self.mapping.is_obstacle(self.x-1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x-1, self.y)
                # self.x = self.x - 1
                self.report_status()
                return True
        elif self.direction == "+y":
            if self.mapping.is_obstacle(self.x, self.y-1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x, self.y-1)
                # self.y = self.y - 1
                self.report_status()
                return True
        elif self.direction == "-x":
            if self.mapping.is_obstacle(self.x+1, self.y):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x+1, self.y)
                # self.x = self.x + 1
                self.report_status()
                return True
        elif self.direction == "-y":
            if self.mapping.is_obstacle(self.x, self.y+1):
                self.report_status()
                return False
            else:
                self.mapping.set_discovered(self.x, self.y)
                self.set_position(self.x, self.y+1)
                # self.y = self.y + 1
                self.report_status()
                return True
        else:
            self.report_status()
            return False

    def turn_left(self):
        if self.direction == "+x":
            self.direction = "+y"
            self.report_status()
            return True
        elif self.direction == "+y":
            self.direction = "-x"
            self.report_status()
            return True
        elif self.direction == "-x":
            self.direction = "-y"
            self.report_status()
            return True
        elif self.direction == "-y":
            self.direction = "+x"
            self.report_status()
            return True
        else:
            self.report_status()
            return False

    def turn_right(self):
        if self.direction == "+x":
            self.direction = "-y"
            self.report_status()
            return True
        elif self.direction == "+y":
            self.direction = "+x"
            self.report_status()
            return True
        elif self.direction == "-x":
            self.direction = "+y"
            self.report_status()
            return True
        elif self.direction == "-y":
            self.direction = "-x"
            self.report_status()
            return True
        else:
            self.report_status()
            return False

    def report_status(self):
        print("{} : {}".format("Input", inputs))
        print("{} : {}".format("Position [x, y]: ", [self.x, self.y]))
        print("{} : {}".format("Direction", self.direction))
        print("Map:")
        self.mapping.print_grid()
        print("\n")

Car = Robot(10, 10, 2, 2)

Car.move_forward()
Car.move_back()
Car.turn_right()
Car.move_back()
