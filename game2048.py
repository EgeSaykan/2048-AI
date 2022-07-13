from copy import deepcopy
import pygame as pg
import functions as fn
pg.init() # initialise pygame
pg.font.init() 

win_width, win_height = 526, 526         # Initialising window width and height
win = pg.display.set_mode((win_width, win_height))  # Initialising the window
pg.display.set_caption("2048")                      # Set the window title to 2048

# get the pressed key and return it
def getInputKey(events, empty, empty2):
    direction = ""
    for event in events:
        if event.key == pg.K_LEFT:
            direction = "LEFT"
        elif event.key == pg.K_RIGHT:
            direction = "RIGHT"
        elif event.key == pg.K_UP:
            direction = "UP"
        elif event.key == pg.K_DOWN:
            direction = "DOWN"
    return direction

# get if key is pressed
def getIfKeyPressed(events):
    for event in events:        
        if event.type == pg.KEYDOWN:
            return True
    return False

# Draws the background colour and the grid lines
def drawBackground():
    pg.init()
    win.fill((227, 220, 200))
    pg.draw.rect(win, (15, 15, 15), (5, 5, 516, 516), 2)
    for i in range(1, 4):
        pg.draw.line(win, (15, 15, 15), (7 + 129 * i, 7), (7 + 129 * i, 526 - 7), 1)
        pg.draw.line(win, (15, 15, 15), (7, 7 + 129 * i), (526 - 7, 7 + 129 * i), 1)

# Draws the numbers depending on the input grid
def drawNumbers(matrix, colourShape):
    font = pg.font.SysFont('Arial',50)
    for i in range(4):
        for m in range(4):
            if matrix[i][m] == 0: number = font.render("0", True, (230, 131, 39))
            else: number = font.render(str(2**(matrix[i][m])), True, (100 + matrix[i][m] * 13, 39 + matrix[i][m] * 6, 20 * colourShape))
            win.blit(number, (25 + m * 129, 32 + i * 129))

# Starts the game when called
class Game2048:
    def __init__(self):
        self.nextMove = False
        self.matrix = [[0 for i in range(4)] for m in range(4)]
        self.repetationCount = 0

    # Returns the result of function name passed in
    def ifNextMove(self, newMoveNoticeFunction, events):
        return newMoveNoticeFunction(events)


def GameLoop2048(directionFunction, newMoveNoticeFunction, gnomeList, nets, ge):
    feedbackCount = 0

    for g in gnomeList:
        # keeps a track of the map, 0 is empty, every other number is interpreted as a power of 2
        fn.randomNumberGeneration(g.matrix)
        fn.randomNumberGeneration(g.matrix)

    # Clock object to set the FPS for the game
    FPS = pg.time.Clock()

    # The last direction player has chosen
    direction = ""

    # Keeps a track of if the game is still on
    run = True

    # Game loop
    while run:

        copylists = deepcopy(gnomeList)

        drawBackground()
        biggest = 0
        for big in range(len(gnomeList)):
            if ge[big].fitness > ge[biggest].fitness: biggest = big
        """for c, g in enumerate(gnomeList):
            if c != biggest: drawNumbers(g.matrix, 2)"""
        drawNumbers(gnomeList[biggest].matrix, 6)

        events = pg.event.get()
        if feedbackCount % 100 >= 99: print(ge[biggest].fitness, gnomeList[biggest].repetationCount)
        for m, gnome in enumerate(gnomeList):
            

            if gnome.ifNextMove(newMoveNoticeFunction, events):
                direction = directionFunction(events, nets[m], gnome.matrix)
                if fn.setNewGrid(gnome.matrix, direction):          # call fn.setNewGrid and check if a new move has been made
                    fn.randomNumberGeneration(gnome.matrix)         # create a new number if a move is made
                    if __name__ != "__main__": ge[m].fitness += fn.evaluateMap(gnome.matrix) * 0.4
                if fn.checkIfLost(gnome.matrix) or gnome.repetationCount >= 20: 
                    run = False   # terminate if there are no available moves
                    if __name__ != "__main__":
                        if m == biggest: print("oh")
                        ge[m].fitness -= 5
                        nets.pop(m)
                        ge.pop(m)
                        gnomeList.pop(m)

                if __name__ != "__main__":
                    if copylists[m].matrix == gnome.matrix: 
                        gnome.repetationCount += 1
                    else: gnome.repetationCount = 0

        for event in events:
            # break if X is pressed
            if event.type == pg.QUIT:
                run = False
                break

        feedbackCount += 1

        # Update the window each frame
        pg.display.update()



if __name__ == "__main__":

    game = Game2048()
    GameLoop2048(getInputKey, getIfKeyPressed, [game], [0], [0])

    # Closes the window
    pg.quit()