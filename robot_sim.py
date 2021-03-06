import pygame
import sys
import random
from pygame.locals import *
from math import *
import Robot
import Drawin

pygame.init()

screen = pygame.display.set_mode((Drawin.Drawin.world_size,
                                 Drawin.Drawin.world_size), 0, 32)
pygame.display.set_caption("Particle filter simulation")


def predict_auto(rob, parts):
    angle = random.random() * 1 - 0.5
    dist = random.random() * 50 + 10
    rob1 = rob.move(angle, dist)
    p1 = []
    for i in range(0, len(parts)):
        p1.append(parts[i].move(angle, dist))
    return rob1, p1


def predict(rob, parts, rot, forw):
    rob1 = rob.move(rot, forw)
    p1 = []
    for i in range(0, len(parts)):
        p1.append(parts[i].move(rot, forw))
    return rob1, p1


def correct(rob, parts):
    z = rob.sense()
    w = []
    for i in range(0, len(parts)):
        w.append(parts[i].measurement_prob(z))

    s = sum(w)
    a = []
    for i in range(0, len(parts)):
        a.append(w[i] / s)

    index = int(random.random() * len(parts))
    b = 0
    maxval = max(a)
    p2 = []
    for i in range(N):
        b = b + random.random() * 2 * maxval
        while b > a[index]:
            b = b - a[index]
            index = index + 1
            if index >= N:
                index = 0
        p2.append(parts[index])
    return p2


myrobot = Robot.Robot(False)
myrobot.set(200, 200, 0.0)
myrobot.set_noise(0.5, 0.1, 15.0)

N = 800
p = []
for i in range(0, N):
    particle = Robot.Robot(True)
    particle.set_noise(0.5, 0.1, 15.0)
    p.append(particle)


Drawin.Drawin.clear(screen)
Drawin.Drawin.draw(screen, myrobot, p)


mainloop = True
while mainloop:
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False
        if event.type == KEYDOWN and event.key == pygame.K_SPACE:
            # Take a screenshot on SPACE key press
            pygame.image.save(screen, "particle_screenshot.png")
        if event.type == KEYDOWN and event.key == pygame.K_LCTRL:
            # Run correction step on CTRL key press
            print("correct")
            p = correct(myrobot, p)
            print(Robot.Robot.eval(myrobot, p))
            Drawin.Drawin.clear(screen)
            Drawin.Drawin.draw(screen, myrobot, p)
        if event.type == KEYDOWN and event.key == pygame.K_LEFT:
            # Run prediction step on Left Arrow key press
            print("predict")
            myrobot, p = predict_auto(myrobot, p)
            Drawin.Drawin.clear(screen)
            Drawin.Drawin.draw(screen, myrobot, p)
        if event.type == KEYDOWN and event.key == pygame.K_UP:
            # Get estimate on Up Arrow key press
            err = Robot.Robot.eval(myrobot, p)
            print("Position error: {:.2f}".format(err))

pygame.quit()
