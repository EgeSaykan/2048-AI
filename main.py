from numpy import matrix, number
import pygame as pg
from sympy import im
import functions as fn
pg.init() # initialise pygame
pg.font.init() 

win_width, win_height, run = 526, 526, True         # Initialising window width, window height and run state of the game
win = pg.display.set_mode((win_width, win_height))  # Initialising the window
pg.display.set_caption("2048")                      # Set the window title to 2048

# keeps a track of the map, 0 is empty, every other number is interpreted as a power of 2
theMatrix = [[0 for i in range(4)] for m in range(4)]
fn.randomNumberGeneration(theMatrix)
fn.randomNumberGeneration(theMatrix)

def drawBackground():
    win.fill((227, 220, 200))
    pg.draw.rect(win, (15, 15, 15), (5, 5, 516, 516), 2)
    for i in range(1, 4):
        pg.draw.line(win, (15, 15, 15), (7 + 129 * i, 7), (7 + 129 * i, 526 - 7), 1)
        pg.draw.line(win, (15, 15, 15), (7, 7 + 129 * i), (526 - 7, 7 + 129 * i), 1)

def drawNumbers():
    font = pg.font.SysFont('Arial',50)
    for i in range(4):
        for m in range(4):
            if theMatrix[i][m] == 0: number = font.render("0", True, (230, 131, 39))
            else: number = font.render(str(2**(theMatrix[i][m])), True, (230, 39, 80))
            win.blit(number, (25 + m * 129, 32 + i * 129))



# Clock object to set the FPS for the game
FPS = pg.time.Clock()

# The last direction player has chosen
direction = ""

# Game loop
while run:
    drawBackground()
    drawNumbers()

    
    for event in pg.event.get():

        # get the pressed key and define direction accordingly
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                direction = "LEFT"
            elif event.key == pg.K_RIGHT:
                direction = "RIGHT"
            elif event.key == pg.K_UP:
                direction = "UP"
            elif event.key == pg.K_DOWN:
                direction = "DOWN"


            if fn.setNewGrid(theMatrix, direction):     # call fn.setNewGrid and check if a new move has been made
                fn.randomNumberGeneration(theMatrix)    # create a new number if a move is made
            if fn.checkIfLost(theMatrix): run = False   # terminate if there are no available moves
        
        # break if X is pressed
        if event.type == pg.QUIT:
            run = False
            break

    # Update the window each frame
    pg.display.update()

pg.quit()
print(theMatrix)