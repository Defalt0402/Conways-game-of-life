import numpy as np
import random
import pygame

# Set display settings
WIDTH = 1000
HEIGHT = 1000
RESOLUTION = 10
CELLS_X = WIDTH // 2
CELLS_Y = HEIGHT // 2

# Create grid to store game
grid = np.zeros((CELLS_Y, CELLS_Y))

# Perform initialisation for pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
running = True

# Create visible grid of 1px border around cells
screen.fill("black")
for i in range(0, CELLS_Y):
    y = i * RESOLUTION
    for j in range(0, CELLS_X):
        x = j * RESOLUTION
        pygame.draw.rect(screen, (0, 0, 0), (x, y, RESOLUTION, RESOLUTION), 1)

# Initialise grid with random values
for i in range(0, CELLS_Y):
    y = i * RESOLUTION
    for j in range(0, CELLS_X):
        x = j * RESOLUTION
        val = random.randint(0, 1)
        grid[i, j] = val
        if val == 1:
            pygame.draw.rect(screen, (255, 255, 255), (x+1, y+1, RESOLUTION-2, RESOLUTION-2))

# Basic game loop
while running:
    # Polling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()