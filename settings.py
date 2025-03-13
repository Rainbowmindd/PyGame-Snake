import pygame

WIDTH,HEIGHT=800,600
GRID_SIZE = 40

# -- colors---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# -- directions --
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

#--other--
MAX_ROUNDS=10
POINTS_PER_APPLE=50
PENALTY=25