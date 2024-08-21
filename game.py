import numpy as np
import pygame

# Set display settings
WIDTH = 1000
HEIGHT = 1000
RESOLUTION = 10

# Create grid to store game
grid = np.zeros((HEIGHT // RESOLUTION, WIDTH // RESOLUTION))

# Perform initialisation for pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Basic game loop
while running:
    # Polling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()