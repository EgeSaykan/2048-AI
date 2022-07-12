import pygame as pg
import functions as fn
pg.init() # initialise pygame
pg.font.init() 

win_width, win_height = 526, 526         # Initialising window width and height
win = pg.display.set_mode((win_width, win_height))  # Initialising the window
pg.display.set_caption("2048")                      # Set the window title to 2048

# get the pressed key and return it
def getInputKey(events):
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
    win.fill((227, 220, 200))
    pg.draw.rect(win, (15, 15, 15), (5, 5, 516, 516), 2)
    for i in range(1, 4):
        pg.draw.line(win, (15, 15, 15), (7 + 129 * i, 7), (7 + 129 * i, 526 - 7), 1)
        pg.draw.line(win, (15, 15, 15), (7, 7 + 129 * i), (526 - 7, 7 + 129 * i), 1)

# Draws the numbers depending on the input grid
def drawNumbers(matrix):
    font = pg.font.SysFont('Arial',50)
    for i in range(4):
        for m in range(4):
            if matrix[i][m] == 0: number = font.render("0", True, (230, 131, 39))
            else: number = font.render(str(2**(matrix[i][m])), True, (100 + matrix[i][m] * 13, 39 + matrix[i][m] * 6, 80))
            win.blit(number, (25 + m * 129, 32 + i * 129))

# Starts the game when called
class Game2048:
    def __init__(self):
        self.nextMove = False
        self.events = pg.event.get()

    # Returns the result of function name passed in
    def ifNextMove(self, newMoveNoticeFunction):
        return newMoveNoticeFunction(self.events)

    def GameLoop2048(self, directionFunction, newMoveNoticeFunction):

        # keeps a track of the map, 0 is empty, every other number is interpreted as a power of 2
        theMatrix = [[0 for i in range(4)] for m in range(4)]
        fn.randomNumberGeneration(theMatrix)
        fn.randomNumberGeneration(theMatrix)

        # Clock object to set the FPS for the game
        FPS = pg.time.Clock()

        # The last direction player has chosen
        direction = ""

        # Keeps a track of if the game is still on
        self.run = True

        # Game loop
        while self.run:
            drawBackground()
            drawNumbers(theMatrix)

            self.events = pg.event.get()

            if self.ifNextMove(newMoveNoticeFunction):
                direction = directionFunction(self.events)
                if fn.setNewGrid(theMatrix, direction):          # call fn.setNewGrid and check if a new move has been made
                    fn.randomNumberGeneration(theMatrix)         # create a new number if a move is made
                if fn.checkIfLost(theMatrix): self.run = False   # terminate if there are no available moves


            for event in self.events:
                # break if X is pressed
                if event.type == pg.QUIT:
                    self.run = False
                    break

            # Update the window each frame
            pg.display.update()

        # Closes the window
        pg.quit()


if __name__ == "__main__":

    game = Game2048()
    game.GameLoop2048(getInputKey, getIfKeyPressed)