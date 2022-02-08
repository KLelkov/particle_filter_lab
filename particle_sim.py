import pygame, sys
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
myrobot.set(200, 200, 0)
myrobot.set_noise(5.0, 0.1, 10.0)
#myrobot.move(pi/4, 50)
#myrobot.move(pi/2, 60)
#myrobot.move(pi/6, -30)

N = 1000
p = []
for i in range(0, N):
    p.append(Robot.Robot(400, True))
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
pygame.quit()
