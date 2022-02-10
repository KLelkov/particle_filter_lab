import random
from math import *

world_size = 400
landmarks  = [[20.0, 20.0], [380.0, 380.0], [20.0, 380.0], [380.0, 20.0]]

class Robot:
    # class wide variables
    particle = False # particle flag, particles should have a different visuals
    path = [] # used to store the robot's traveled path
    # Actual parameters
    x = 0.0
    y = 0.0
    orientation = 0.0
    forward_noise = 0.0
    turn_noise = 0.0
    sense_noise = 0.0


    def __init__(self, particle = False):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0
        # Graphic stuff
        self.path = []
        self.path.append((self.x, self.y))
        self.particle = particle


    def set(self, new_x, new_y, new_orientation):
        new_x %= world_size    # cyclic truncate
        new_y %= world_size
        new_orientation %= 2*pi
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        self.path = []
        self.path.append((self.x, self.y))

    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise    = float(new_t_noise)
        self.sense_noise   = float(new_s_noise)

    def move(self, turn, forward):
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        #print(self.orientation)
        x = self.x + (cos(self.orientation) * dist)
        y = self.y + (sin(self.orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        self.path.append((x, y))
        #print(self.x)
        part = Robot(self.particle)
        part.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        part.set(x, y, orientation)
        part.path = self.path
        return part


    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))


    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob


    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))


    def eval(r, p):
        sum = 0.0;
        for i in range(len(p)): # calculate mean error
            dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
            dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
            err = sqrt(dx * dx + dy * dy)
            sum += err
        return sum / float(len(p))
