import numpy as np
import random
import pygame
import math

# Set display settings
GAMEWIDTH = 1000
WIDTH = 1400
HEIGHT = 1000
RESOLUTION = 10
CELLS_X = GAMEWIDTH // RESOLUTION
CELLS_Y = HEIGHT // RESOLUTION
FPS = 30

# Create grid to store game
grid = np.zeros((CELLS_Y, CELLS_X))

# Perform initialisation for pygame
pygame.init()
pygame.font.init()
# Define 3 font sizes
fontLarge = pygame.font.SysFont(None, 50)
fontMedium = pygame.font.SysFont(None, 40)
fontSmall = pygame.font.SysFont(None, 29)
# Set window attributes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
running = True
coloured = False

# Create visible grid of 1px border around cells
screen.fill("black")
for i in range(CELLS_Y):
    y = i * RESOLUTION
    for j in range(CELLS_X):
        x = j * RESOLUTION
        pygame.draw.rect(screen, (0, 0, 0), (x, y, RESOLUTION, RESOLUTION), 1)

# Initialises the grid with random values
def initialise_grid():
    global grid
    for i in range(0, CELLS_Y):
        for j in range(0, CELLS_X):
            grid[i, j] = random.randint(0, 1)
    draw_grid()

# Draw everything onto the grid
def draw_grid():
    global grid, coloured
    for i in range(CELLS_Y):
        for j in range(CELLS_X):
            # Actual positions of the visible grid square
            x = j * RESOLUTION
            y = i * RESOLUTION

            # Set colour if coloured flag is True
            colour = get_cell_colour(j, i) if coloured else (255, 255, 255)

            if grid[i, j] == 1:
                # Draw at x and y + 1 with Resolution - 2 in order to not hide the grid lines
                pygame.draw.rect(screen, colour, (x+1, y+1, RESOLUTION-2, RESOLUTION-2))
            else:
                pygame.draw.rect(screen, (0, 0, 0) , (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

# Sets all cells to 0
def clear_grid():
    global grid

    grid.fill(0)

    draw_grid()

# Maps grid position to r, g, b values
# Right = red, left = blue, bottom = green
def get_cell_colour(x, y):
    r = (x * 255) // CELLS_X
    g = (y * 255) // CELLS_Y
    b = 255 - r

    return(r, g, b)

# Fills grid with all 1s
def fill_grid():
    global grid
    grid.fill(1)


# Draw the grid and information panel at the side
initialise_grid()

pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 1000), 2)
title = fontLarge.render("Conway's Game of Life", True, (255, 255, 255))
titleRect = title.get_rect()
titleRect.center = (1200, 50)
screen.blit(title, titleRect)

# Text explaining controls
pauseText = fontSmall.render("To pause and unpause, press: Space", True, (255, 255, 255))
clearText = fontSmall.render("To clear the grid, press: C", True, (255, 255, 255))
randomText = fontSmall.render("To randomise the grid, press: R", True, (255, 255, 255))
fillText = fontSmall.render("To fill the grid, press: F", True, (255, 255, 255))
colourText = fontSmall.render("To colourise the grid, press: G", True, (255, 255, 255))
drawText = fontSmall.render("To draw on the grid, left click on a cell", True, (255, 255, 255))
eraseText = fontSmall.render("To erase from the grid, left click on a cell", True, (255, 255, 255))
exitText = fontSmall.render("To close the game, press: Q", True, (255, 255, 255))

# Text requires a rect to be placed on screen
# Each block gets the rect and sets its position for each piece of info text
pauseRect = pauseText.get_rect()
pauseRect.center = (1200, 300)
screen.blit(pauseText, pauseRect)

clearRect = clearText.get_rect()
clearRect.center = (1200, 350)
screen.blit(clearText, clearRect)

randomRect = randomText.get_rect()
randomRect.center = (1200, 400)
screen.blit(randomText, randomRect)

fillRect = fillText.get_rect()
fillRect.center = (1200, 450)
screen.blit(fillText, fillRect)

colourRect = colourText.get_rect()
colourRect.center = (1200, 500)
screen.blit(colourText, colourRect)

drawRect = drawText.get_rect()
drawRect.center = (1200, 550)
screen.blit(drawText, drawRect)

eraseRect = eraseText.get_rect()
eraseRect.center = (1200, 600)
screen.blit(eraseText, eraseRect)

exitRect = exitText.get_rect()
exitRect.center = (1200, 800)
screen.blit(exitText, exitRect)

pygame.display.flip()

# Main game loop
def game_loop(leftMouseHeld=None, rightMouseHeld=None):
    global running, grid, coloured

    # Tell user game is running
    pygame.draw.rect(screen, (0, 0, 0) , (1010, 110, 1390, 150))
    runningText = fontMedium.render("Game is Running", True, (255, 255, 255))
    runningTextRect = runningText.get_rect()
    runningTextRect.center = (1200, 150)
    screen.blit(runningText, runningTextRect)

    # Check if user is holding the mouse down
    if leftMouseHeld == None:
        # Create Flags used for drawing
        leftMouseHeld = False
        rightMouseHeld = False

    # Basic game loop
    while running:
        # Polling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
                    break
                elif event.key == pygame.K_c:
                    clear_grid()
                elif event.key == pygame.K_r:
                    initialise_grid()
                elif event.key == pygame.K_f:
                    fill_grid() 
                elif event.key == pygame.K_g:
                    coloured = not coloured
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()

            # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    leftMouseHeld = True
                elif event.button == 3:
                    rightMouseHeld = True

            # Check for mouse button releases
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    leftMouseHeld = False
                elif event.button == 3:
                    rightMouseHeld = False
        
        # Pause game
        if running == False:
            break

        # Update all cells
        newGrid = np.copy(grid)
        paddedGrid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
        for i in range(1, CELLS_Y + 1):
            for j in range(1, CELLS_X + 1):
                # Get ROI, accounting for corners and edges
                roi = paddedGrid[i-1:i+2, j-1:j+2]

                # Get number of living neighbours, remove 1 if origin is 1
                neighbours = np.sum(roi) - roi[1, 1]

                # Apply rules
                if roi[1, 1] == 1:
                    if neighbours < 2 or neighbours > 3:
                        newGrid[i-1, j-1] = 0
                elif roi[1, 1] == 0:
                    if neighbours == 3:
                        newGrid[i-1, j-1] = 1

        # Update grid
        grid = newGrid
                
        # Draw on grid if mouse is being held
        if leftMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX <= GAMEWIDTH and mouseY >= 0 and mouseY <= HEIGHT:
                # Translate mouse position to corresponding grid position
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = 1

        # erase from grid if mouse is being held
        if rightMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX <= GAMEWIDTH and mouseY >= 0 and mouseY <= HEIGHT:
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = 0
    
        draw_grid()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    # If Game is paused
    while not running:

        # Tell user game is paused
        pygame.draw.rect(screen, (0, 0, 0) , (1010, 110, 1390, 150))
        runningText = fontMedium.render("Game is Paused", True, (255, 255, 255))
        runningTextRect = runningText.get_rect()
        runningTextRect.center = (1200, 150)
        screen.blit(runningText, runningTextRect)

        # Polling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                    break
                elif event.key == pygame.K_c:
                    clear_grid()
                elif event.key == pygame.K_r:
                    initialise_grid()
                elif event.key == pygame.K_f:
                    fill_grid()    
                elif event.key == pygame.K_g:
                    coloured = not coloured
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()

            # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    leftMouseHeld = True
                elif event.button == 3:
                    rightMouseHeld = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    leftMouseHeld = False
                elif event.button == 3:
                    rightMouseHeld = False
        
        if running == True:
            game_loop(leftMouseHeld, rightMouseHeld)

        if leftMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX <= GAMEWIDTH and mouseY >= 0 and mouseY <= HEIGHT:
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = 1

        if rightMouseHeld:
            mouseX, mouseY = pygame.mouse.get_pos()
            # If mouse is in bounds
            if mouseX >= 0 and mouseX <= GAMEWIDTH and mouseY >= 0 and mouseY <= HEIGHT:
                cellX = mouseX // RESOLUTION
                cellY = mouseY // RESOLUTION
                grid[cellY, cellX] = 0
        
        

        draw_grid()

        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

game_loop()