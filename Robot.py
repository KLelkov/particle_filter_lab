import pygame, random
from math import *

class Robot:
    # class wide variables
    size = 12 # robot size
    color = (73, 146, 104) # robot color
    pathcolor = (40, 45, 50)
    # Vector image of a robot
    bodyTemplate = [(0.6, 0), (0, 0.2), (-0.2, 0.5), (-0.4, 0.2), (-0.4, -0.2), (-0.2, -0.5), (0, -0.2), (0.6, 0)]
    particle = False # particle flag, particles should have a different visuals
    path = [] # used to store the robot's traveled path
    # Actual parameters
    x = 0.0
    y = 0.0
    orientation = 0.0
    forward_noise = 0.0
    turn_noise = 0.0
    sense_noise = 0.0


    def __init__(self, world_size = 400, particle = False):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0
        self.world_size = world_size
        # Graphic stuff
        self.path = []
        self.path.append((self.x, self.y))
        self.bodyState = list(self.bodyTemplate)
        self.bodyGrid = [(0, 0) for ln in range(8)]
        if particle:
            self.color = (180, 101, 74)
            self.particle = True
        self.gridUpdate()


    def set(self, new_x, new_y, new_orientation):
        new_x %= self.world_size    # cyclic truncate
        new_y %= self.world_size
        new_orientation %= 2*pi
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
        self.path = []
        self.path.append((self.x, self.y))
        self.gridUpdate()

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
        self.orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        self.orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        self.x = self.x + (cos(self.orientation) * dist)
        self.y = self.y + (sin(self.orientation) * dist)
        self.x %= self.world_size    # cyclic truncate
        self.y %= self.world_size
        self.path.append((self.x, self.y))
        # Update image
        self.gridUpdate()

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

    def gridUpdate(self):
        #list(self.bodyTemplate)
        bodyVector = list(self.bodyTemplate)
        #for point in range(0, 8):
        #    bodyVector.append((self.bodyState[point][0], self.bodyState[point][1]))
        for point in range(0, 8):
            self.bodyState[point] = \
                ((bodyVector[point][0] * cos(self.orientation) - bodyVector[point][1] * sin(self.orientation),
                  bodyVector[point][0] * sin(self.orientation) + bodyVector[point][1] * cos(self.orientation)))
        for point in range(0, 8):
            self.bodyGrid[point] = (self.bodyState[point][0]*self.size + self.x,
                                    self.bodyState[point][1]*self.size + self.y)

    def draw(self, screenHandle):
        if len(self.path) > 2 and self.particle == False:
            pygame.draw.aalines(screenHandle, self.pathcolor, False, self.path)
        pygame.draw.aalines(screenHandle, self.color, True, self.bodyGrid)
        if not self.particle:
            pygame.draw.polygon(screenHandle, self.color, self.bodyGrid, 0)
        #pygame.draw.aalines(screenHandle, self.color, True, self.towerGrid)


    def gridRotate(self, angle):
        bodyVector = []
        for point in range(0, 8):
            bodyVector.append((self.bodyState[point][0], self.bodyState[point][1]))
        for point in range(0, 8):
            self.bodyState[point] = \
                ((bodyVector[point][0] * cos(angle) - bodyVector[point][1] * sin(angle),
                  bodyVector[point][0] * sin(angle) + bodyVector[point][1] * cos(angle)))
        self.gridUpdate()

    def eval(r, p):
        sum = 0.0;
        for i in range(len(p)): # calculate mean error
            dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
            dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
            err = sqrt(dx * dx + dy * dy)
            sum += err
        return sum / float(len(p))
