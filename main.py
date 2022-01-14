import matplotlib.pyplot as plt
import math

# Constants
G = 9.80
PI = math.pi
ORIGIN = [0, 0]
T = 0.015 # time step

# Simple Pendulum
class Pendulum:

    def __init__(self, a, r):
        """
        a: angle of pendulum. (0 = vertical downwards, counter-clockwise is positive)
        r = length of rod
        """
        self.a = a
        self.r = r

        # Angular Velocity and Acceleration
        self.a_v = 0
        self.a_a = 0

    def update(self):
        # Moves the pendulum one time step
        self.a_a = -G / self.r * math.sin(self.a)
        self.a_v += self.a_a
        self.a += self.a_v

    def get_coord(self):
        # Returns cartesian point, from angle and rod length
        # Assumes that rod is rooted at the origin (0,0)
        x = self.r * math.sin(self.a)
        y = -self.r * math.cos(self.a)
        return [x, y]


class DoublePendulum:

    def __init__(self, a1, a2, r1, r2):
        """
        a1: angle of pendulum 1
        a2: angle of pendulum 2
        r1: rod length of pendulum 1
        r2: rod length of pendulum 2
        """

        # Position
        self.a1 = a1
        self.a2 = a2
        self.r1 = r1
        self.r2 = r2

        self.m1 = 1.0
        self.m2 = 1.0

        # Acceleration and velocity
        self.a1_v = 0.0
        self.a2_v = 0.0
        self.a1_a = 0.0
        self.a2_a = 0.0

    def update(self):
        # The motion of a pendulum can be modelled using an equation,
        # however, these equations are long, so we break them up into components to calculate angular acceleration

        # Acceleration of mass 1
        num1 = -G * (2*self.m1 + self.m2) * math.sin(self.a1)
        num2 = -self.m2 * G * math.sin(self.a1 - 2*self.a2)
        num3 = -2 * math.sin(self.a1 - self.a2) * self.m2
        num4 = self.a2_v * self.a2_v * self.r2 + self.a1_v * self.a1_v * self.r1 * math.cos(self.a1 - self.a2)
        den = self.r1 * (2*self.m1 + self.m2 - self.m2 * math.cos(2*self.a1 - 2*self.a2))

        self.a1_a = (num1 + num2 + num3 * num4) / den

        # Acceleration of mass 2
        num1 = 2 * math.sin(self.a1 - self.a2)
        num2 = self.a1_v * self.a1_v * self.r1 * (self.m1 + self.m2)
        num3 = G * (self.m1 + self.m2) * math.cos(self.a1)
        num4 = self.a2_v * self.a2_v * self.r2 * self.m2 * math.cos(self.a1 - self.a2)
        den = self.r2 * (2*self.m1 + self.m2 - self.m2 * math.cos(2*self.a1 - 2*self.a2))

        self.a2_a = num1 * (num2 + num3 + num4) / den

        # Now update angular position
        self.a1 = self.a1 + self.a1_v*T + 0.5*self.a1_a*T*T
        self.a2 = self.a2 + self.a2_v*T + 0.5*self.a2_a*T*T

        # We update velocities last
        self.a1_v += self.a1_a * T
        self.a2_v += self.a2_a * T

        # Keep angles in domain of one circle
        self.a1 = self.a1 % (2*PI)
        self.a2 = self.a2 % (2*PI)

    def get_coords(self):

        x1 = self.r1 * math.sin(self.a1)
        y1 = -self.r1 * math.cos(self.a1)

        x2 = x1 + self.r2 * math.sin(self.a2)
        y2 = y1 + (-self.r2 * math.cos(self.a2))

        return [x1, x2], [y1, y2]


# p = Pendulum(PI/2, 5.00)
a1 = 3*PI/4
a2 = PI/3
r1 = 1.00
r2 = 1.00
dp = DoublePendulum(a1, a2, r1, r2)

# Time to run in seconds
sim_length = 20
FPS = 120

for i in range(FPS * sim_length):
    x, y = dp.get_coords()

    plt.xlim(-2.5, 2.5)
    plt.ylim(-2.5, 2.5)
    plt.grid()

    plt.plot([0, x[0]], [0, y[0]], color='black')
    plt.plot(x, y, color='blue')
    plt.scatter(x, y, s=50, color='black')
    plt.pause(1.00/FPS)

    dp.update()
    plt.clf()

plt.show()
