import pygame

class Feature:
    # class wide variables
    size = 30
    color = (32, 42, 68)
    polygonTemplate = [(-0.25, -0.5), (0.25, -0.5), (0.5, -0.25), (0.5, 0.25), (0.25, 0.5), (-0.25, 0.5), (-0.5, 0.25), (-0.5, -0.25)]

    def __init__(self, position):
        self.position = position
        self.polygonGrid = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        for point in range(0, 8):
            self.polygonGrid[point] = (self.polygonTemplate[point][0]*self.size + self.position[0],
                                       self.polygonTemplate[point][1]*self.size + self.position[1])

    def draw(self, screenHandle):
        pygame.draw.aalines(screenHandle, self.color, True, self.polygonGrid)
        for ln in range(0,4):
            pygame.draw.aaline(screenHandle, self.color, self.polygonGrid[ln], self.polygonGrid[ln+4])
