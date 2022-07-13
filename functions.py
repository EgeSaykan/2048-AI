from random import choice, randint
from copy import deepcopy

# adds to direction given as string: RIGHT, LEFT, UP, DOWN
def addTheGrid(map, direction):    

    if direction == 'RIGHT':
        for c in range(len(map)):
            for m in range(3, 0, -1):
                for k in range(1, 1 + m):
                    if map[c][m] == map[c][m-k] and map[c][m] != 0:
                        map[c][m] += 1
                        map[c][m - k] = 0
                        break
                    elif map[c][m] != map[c][m-k] and map[c][m] != 0 and map[c][m-k] != 0: break

    elif direction == 'LEFT':    
        for c in range(len(map)):
            for m in range(0, 3):
                for k in range(1, 4 - m):
                    if map[c][m] == map[c][m+k] and map[c][m] != 0:
                        map[c][m] += 1
                        map[c][m + k] = 0    
                        break
                    elif map[c][m] != map[c][m+k] and map[c][m] != 0 and map[c][m+k] != 0: break
    
    elif direction == 'UP':    
        for m in range(len(map[0])):
            for c in range(0, 3):
                for k in range(1, 4 - c):
                    if map[c][m] == map[c+k][m] and map[c][m] != 0:
                        map[c][m] += 1
                        map[c + k][m] = 0    
                        break
                    elif map[c][m] != map[c+k][m] and map[c][m] != 0 and map[c+k][m] != 0: break

    elif direction == 'DOWN':    
        for m in range(len(map[0])):
            for c in range(3, 0, -1):
                for k in range(1, 1 + c):
                    if map[c][m] == map[c-k][m] and map[c][m] != 0:
                        map[c][m] += 1
                        map[c - k][m] = 0    
                        break
                    elif map[c][m] != map[c-k][m] and map[c][m] != 0 and map[c-k][m] != 0: break


# Evaluates the score
def evaluateMap(map):
    avarage = 0
    for i in map: 
        for m in i: 
            avarage += m / 16
    
    centre_of_mass = (map[0][0] * 8 + map[0][1] * 4 + map[1][0] * 4 + map[1][1] * 2) * 2 + (map[3][0] * 8 + map[3][1] * 4 + map[2][0] * 4 + map[2][1] * 2) + (map[0][3] * 8 + map[0][2] * 4 + map[1][3] * 4 + map[2][1] * 2) + (map[3][3] * 8 + map[3][2] * 4 + map[2][3] * 4 + map[2][2] * 2)
    centre_of_mass /= 4

    return centre_of_mass * avarage




# then moves the numbers to empty boxes to direction given as string: RIGHT, LEFT, UP, DOWN
def moveTheGrid(map, direction):
    if direction == 'RIGHT':
        for i in range(len(map)):
            for m in range(2, -1, -1):                
                for k in range(3, m, -1):
                    if map[i][k] == 0:
                        map[i][k] = map[i][m]
                        map[i][m] = 0
                        break
    
    elif direction == 'LEFT':
        for i in range(len(map)):
            for m in range(1, 4):                
                for k in range(m):
                    if map[i][k] == 0:
                        map[i][k] = map[i][m]
                        map[i][m] = 0
                        break

    elif direction == 'UP':
        for i in range(len(map)):
            for m in range(1, 4):
                for k in range(m):
                    if map[k][i] == 0:
                        map[k][i] = map[m][i]
                        map[m][i] = 0
                        break

    elif direction == 'DOWN':
        for i in range(len(map)):
            for m in range(2, -1, -1):                
                for k in range(3, m, -1):
                    if map[k][i] == 0:
                        map[k][i] = map[m][i]
                        map[m][i] = 0
                        break


# firstly calls addTheGrid() function to add the necessary boxes
# then calls moveTheGrid() function to fill in the empty boxes
# returns true if a move is made, false if no move is made
def setNewGrid(map, direction):
    fmap = deepcopy(map)
    addTheGrid(map, direction)
    moveTheGrid(map, direction)
    if fmap == map:
        return False
    return True


# creates a new number on the grid
def randomNumberGeneration(map):
    emptyspots = []
    for i in range(4):
        for m in range(4):
            if map[i][m] == 0: emptyspots.append((i, m))
    
    randomIndex = choice(emptyspots)

    # chosing randomly between 4 or 2, chance for 2 is 90%, chance for 4 is 10%
    twoOrFour = randint(1, 10)
    if twoOrFour > 9: map[randomIndex[0]][randomIndex[1]] = 2
    else: map[randomIndex[0]][randomIndex[1]] = 1

# checks if there are any available moves
def checkIfLost(map):
    copy1, copy2, copy3, copy4 = [deepcopy(map) for i in range(4)]
    setNewGrid(copy1, "RIGHT")
    setNewGrid(copy2, "LEFT")
    setNewGrid(copy3, "UP")
    setNewGrid(copy4, "DOWN")

    # returns True if both of the copies are same as initial grid
    if copy1 == map and copy2 == map and copy3 == map and copy4 == map:
        return True
    return False 