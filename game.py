import numpy as np
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

screen.fill("black")
for i in range(0, CELLS_Y):
    y = i * RESOLUTION
    for j in range(0, CELLS_X):
        x = j * RESOLUTION
        pygame.draw.rect(screen, (0, 0, 0), (x, y, RESOLUTION, RESOLUTION), 1)

# Basic game loop
while running:
    # Polling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()