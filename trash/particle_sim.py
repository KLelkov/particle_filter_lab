import pygame, sys, random
from pygame.locals import *
from math import *
import Map, Robot, Feature

world_size = 400
landmarks  = [[20.0, 20.0], [380.0, 380.0], [20.0, 380.0], [380.0, 20.0]]

pygame.init()

screen = pygame.display.set_mode((world_size,world_size), 0, 32)
pygame.display.set_caption("Particle filter simulation")

Map.Map.init()
features = []
for feature in landmarks:
    features.append(Feature.Feature(feature))


myrobot = Robot.Robot(400, False)
myrobot.set(200,200, 0)
myrobot.set_noise(5.0, 0.1, 10.0)

N = 1000
p = []

for i in range(0, N):
    particle = Robot.Robot(400, True)
    particle.set_noise(0.0, 0.0, 10.0)
    p.append(particle)

Z = myrobot.sense(landmarks)
w = []
for i in range(0, N):
    w.append(p[i].measurement_prob(Z, landmarks))

s = sum(w)
a = []
for i in range(0, N):
    a.append(w[i] / s)



#for part in p:
    #part.set_noise(5.0, 0.1, 10.0)
    #part.move(pi/4, 50)
    #part.move(pi/2, 60)
    #part.move(pi/6, -30)
Map.Map.clear(screen)
for pa in p:
    pa.draw(screen)
myrobot.draw(screen)
for feature in features:
    feature.draw(screen)
# essential
pygame.display.update()

mainloop = True
while mainloop:
    for event in pygame.event.get():
        if event.type == QUIT:
            mainloop = False
        if event.type == KEYDOWN and event.key == pygame.K_SPACE:
            pygame.image.save(screen, "particle_screenshot.png")
        if event.type == KEYDOWN and event.key == pygame.K_LCTRL:
            Z = myrobot.sense(landmarks)
            w = []
            for i in range(0, N):
                w.append(p[i].measurement_prob(Z, landmarks))

            s = sum(w)
            a = []
            for i in range(0, N):
                a.append(w[i] / s)

            index = int(random.random() * N)
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
                p2.append(p[index])
            p = p2
            Map.Map.clear(screen)
            for i in range(0, N):
                #print(p[i].x)
                p[i].draw(screen)
            myrobot.draw(screen)
            for feature in features:
                feature.draw(screen)
            # essential
            pygame.display.update()
        if event.type == KEYDOWN and event.key == pygame.K_LEFT:
            angle = random.random() * 0.3
            myrobot.move(angle, 50)
            #Map.Map.clear(screen)
            print("once")
            p2 = []
            for i in range(0, N):
                p2.append(p[i].move(angle, 50))
                #p[i].move(angle, 50)
                #p[i].draw(screen)
                #print(p[i].x)
            p = p2
            for i in range(0, N):
                print(p2[i].x)
            #print(p[2].forward_noise)
            Map.Map.clear(screen)
            for i in range(0, N):
                #print(p[i].x)
                p2[i].draw(screen)
            myrobot.draw(screen)
            for feature in features:
                feature.draw(screen)
            # essential
            pygame.display.update()


pygame.quit()
