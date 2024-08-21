import numpy as np
import random
import pygame

# Set display settings
GAMEWIDTH = 1000
WIDTH = 1400
HEIGHT = 1000
RESOLUTION = 10
CELLS_X = GAMEWIDTH // RESOLUTION
CELLS_Y = HEIGHT // RESOLUTION

# Create grid to store game
grid = np.zeros((CELLS_Y, CELLS_X))

# Perform initialisation for pygame
pygame.init()
pygame.font.init()
fontLarge = pygame.font.SysFont(None, 50)
fontMedium = pygame.font.SysFont(None, 40)
fontSmall = pygame.font.SysFont(None, 29)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
running = True

# Create visible grid of 1px border around cells
screen.fill("black")
for i in range(CELLS_Y):
    y = i * RESOLUTION
    for j in range(CELLS_X):
        x = j * RESOLUTION
        pygame.draw.rect(screen, (0, 0, 0), (x, y, RESOLUTION, RESOLUTION), 1)

def initialise_grid():
    global grid
    # Initialise grid with random values
    for i in range(0, CELLS_Y):
        for j in range(0, CELLS_X):
            val = random.randint(0, 1)
            grid[i, j] = val
    draw_grid()

# Draw everything onto the grid
def draw_grid():
    global grid
    for i in range(CELLS_Y):
        for j in range(CELLS_X):
            x = j * RESOLUTION
            y = i * RESOLUTION
            if grid[i, j] == 1:
                pygame.draw.rect(screen, (255, 255, 255) , (x+1, y+1, RESOLUTION-2, RESOLUTION-2))
            else:
                pygame.draw.rect(screen, (0, 0, 0) , (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

def clear_grid():
    global grid

    grid = np.zeros((CELLS_Y, CELLS_X))

    draw_grid()

# Draw the grid and information panel at the side
initialise_grid()

pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 1000), 2)
title = fontLarge.render("Conway's Game of Life", True, (255, 255, 255))
titleRect = title.get_rect()
titleRect.center = (1200, 50)
screen.blit(title, titleRect)

pauseText = fontSmall.render("To pause and unpause, press: Space", True, (255, 255, 255))
clearText = fontSmall.render("To clear the grid, press: C", True, (255, 255, 255))
randomText = fontSmall.render("To randomise the grid, press: R", True, (255, 255, 255))
drawText = fontSmall.render("To draw on the grid, left click on a cell", True, (255, 255, 255))
eraseText = fontSmall.render("To erase from the grid, left click on a cell", True, (255, 255, 255))

pauseRect = pauseText.get_rect()
pauseRect.center = (1200, 300)
screen.blit(pauseText, pauseRect)

clearRect = clearText.get_rect()
clearRect.center = (1200, 350)
screen.blit(clearText, clearRect)

randomRect = randomText.get_rect()
randomRect.center = (1200, 400)
screen.blit(randomText, randomRect)

drawRect = drawText.get_rect()
drawRect.center = (1200, 450)
screen.blit(drawText, drawRect)

eraseRect = eraseText.get_rect()
eraseRect.center = (1200, 500)
screen.blit(eraseText, eraseRect)


pygame.display.flip()

def game_loop():
    global running, grid

    # Tell user game is running
    pygame.draw.rect(screen, (0, 0, 0) , (1010, 110, 1390, 150))
    runningText = fontMedium.render("Game is Running", True, (255, 255, 255))
    runningTextRect = runningText.get_rect()
    runningTextRect.center = (1200, 150)
    screen.blit(runningText, runningTextRect)

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
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()

            # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Left mouse button clicked")
                elif event.button == 3:
                    print("Right mouse button clicked")
        
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

        grid = newGrid
                
        draw_grid()

        pygame.display.flip()

        clock.tick(30)  # limits FPS to 60

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
                    running = False
                    break
                elif event.key == pygame.K_c:
                    clear_grid()
                elif event.key == pygame.K_r:
                    initialise_grid()
                elif event.key == pygame.K_q:
                    running = False
                    pygame.quit()

            # Check for mouse button presses
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print("Left mouse button clicked")
                elif event.button == 3:
                    print("Right mouse button clicked")
        
        if running == True:
            game_loop()

        draw_grid()

        pygame.display.flip()

        clock.tick(30)  # limits FPS to 60

game_loop()