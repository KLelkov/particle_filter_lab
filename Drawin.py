import pygame
from math import *


class Drawin:
    # class wide variables
    robot_size = 12 # robot size
    robot_color = (73, 146, 104) # robot color
    pathcolor = (40, 45, 50)
    particle_color = (180, 101, 74)
    # Vector image of a robot
    robot_Template = [(0.6, 0), (0, 0.2), (-0.2, 0.5), (-0.4, 0.2), (-0.4, -0.2), (-0.2, -0.5), (0, -0.2), (0.6, 0)]
    # Actual parameters
    world_size = 400
    landmarks  = [[20.0, 20.0], [380.0, 580.0], [20.0, 380.0], [380.0, 20.0]]
    cellSize = 50
    backgroundColor = (214, 217, 207)
    delimiterColor = (234, 237, 237)
    feature_size = 30
    feature_color = (32, 42, 68)
    feature_Template = [(-0.25, -0.5), (0.25, -0.5), (0.5, -0.25), (0.5, 0.25), (0.25, 0.5), (-0.25, 0.5), (-0.5, 0.25), (-0.5, -0.25)]


    @staticmethod
    def clear(screenHandle):
        screenHandle.fill(Drawin.backgroundColor)
        horizontalLen = Drawin.world_size / Drawin.cellSize
        verticalLen = Drawin.world_size / Drawin.cellSize
        for hor in range(1, verticalLen):
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((0, Drawin.cellSize * hor - 1), (Drawin.world_size, Drawin.cellSize * hor - 1)))
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((0, Drawin.cellSize * hor), (Drawin.world_size, Drawin.cellSize * hor)))
        for ver in range(1, horizontalLen):
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((Drawin.cellSize * ver - 1, 0), (Drawin.cellSize * ver - 1, Drawin.world_size)))
            pygame.draw.aalines(screenHandle, Drawin.delimiterColor, False,
                                ((Drawin.cellSize * ver, 0), (Drawin.cellSize * ver, Drawin.world_size)))


    @staticmethod
    def draw(screenHandle, rob, parts):
        # Draw obstacles
        for feature in Drawin.landmarks:
            polygonGrid = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
            for point in range(0, 8):
                polygonGrid[point] = (Drawin.feature_Template[point][0]*Drawin.feature_size + feature[0],
                                           Drawin.feature_Template[point][1]*Drawin.feature_size + feature[1])
            pygame.draw.aalines(screenHandle, Drawin.feature_color, True, polygonGrid)
            for ln in range(0,4):
                pygame.draw.aaline(screenHandle, Drawin.feature_color, polygonGrid[ln], polygonGrid[ln+4])

        # Draw partiles
        for i in range(0, len(parts)):
            partGrid = Drawin.getGrid(parts[i])
            pygame.draw.aalines(screenHandle, Drawin.particle_color, True, partGrid)

        # Draw robot
        robotGrid = Drawin.getGrid(rob)
        if len(rob.path) > 1 and rob.particle == False:
            pygame.draw.aalines(screenHandle, Drawin.pathcolor, False, rob.path)
        pygame.draw.aalines(screenHandle, Drawin.robot_color, True, robotGrid)
        pygame.draw.polygon(screenHandle, Drawin.robot_color, robotGrid, 0)

        # essential
        pygame.display.update()


    @staticmethod
    def getGrid(part):
        bodyVector = list(Drawin.robot_Template)
        robotGrid = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        for point in range(0, 8):
            robotGrid[point] = \
                ((bodyVector[point][0] * cos(part.orientation) - bodyVector[point][1] * sin(part.orientation)) * Drawin.robot_size + part.x,
                  (bodyVector[point][0] * sin(part.orientation) + bodyVector[point][1] * cos(part.orientation)) * Drawin.robot_size + part.y)
        return robotGrid
