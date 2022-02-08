import pygame, copy

class Map:
    height = 400
    width = 400
    cellSize = 50
    backgroundColor = (214, 217, 207)
    delimiterColor = (234, 237, 237)
    layout = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
              [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
              [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
              [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
    state = layout
    obstacleList = []

    @staticmethod
    def init():
        a = 0
        #rows = len(Map.layout)
        #cols = len(Map.layout[0])
        #for row in range(0, rows):
            #for col in range(0, cols):
                #if Map.layout[row][col] == 1:
                    # It may be confusing, but if you think about it - row index is actually
                    # indicating vertical coordinate Y, and column index equals X
                    #Map.obstacleList.append(Obstacle.Obstacle((col * Map.cellSize, row * Map.cellSize)))


    @staticmethod
    def clear(screenHandle):
        screenHandle.fill(Map.backgroundColor)
        horizontalLen = Map.width / Map.cellSize
        verticalLen = Map.height / Map.cellSize
        for hor in range(1, verticalLen):
            pygame.draw.aalines(screenHandle, Map.delimiterColor, False,
                                ((0, Map.cellSize * hor - 1), (Map.width, Map.cellSize * hor - 1)))
            pygame.draw.aalines(screenHandle, Map.delimiterColor, False,
                                ((0, Map.cellSize * hor), (Map.width, Map.cellSize * hor)))
        for ver in range(1, horizontalLen):
            pygame.draw.aalines(screenHandle, Map.delimiterColor, False,
                                ((Map.cellSize * ver - 1, 0), (Map.cellSize * ver - 1, Map.height)))
            pygame.draw.aalines(screenHandle, Map.delimiterColor, False,
                                ((Map.cellSize * ver, 0), (Map.cellSize * ver, Map.height)))
        #for obstacle in Map.obstacleList:
        #    obstacle.draw(screenHandle)
        Map.state = copy.deepcopy(Map.layout)

    @staticmethod
    def updateState(newObject):
        d = 3
        #gridPos = Map.pos2grid(newObject.position)
        #Map.state[gridPos[0]][gridPos[1]] = newObject.mapID
