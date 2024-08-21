import numpy as np
import random
import pygame

# Set display settings
WIDTH = 1000
HEIGHT = 1000
RESOLUTION = 10
CELLS_X = WIDTH // RESOLUTION
CELLS_Y = HEIGHT // RESOLUTION

# Create grid to store game
grid = np.zeros((CELLS_Y, CELLS_X))

# Perform initialisation for pygame
pygame.init()
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

# Initialise grid with random values
for i in range(0, CELLS_Y):
    for j in range(0, CELLS_X):
        val = random.randint(0, 1)
        grid[i, j] = val

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

draw_grid()
pygame.display.flip()

# Basic game loop
while running:
    # Polling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

pygame.quit()