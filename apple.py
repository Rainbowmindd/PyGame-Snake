import random
import pygame
from settings import GRID_SIZE, WIDTH, HEIGHT,RED

class Apple:
    def __init__(self):
        self.position = self.randomize_position()
        
    def randomize_position(self):
        return (
            random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )
        
    def draw(self, display):
        pygame.draw.rect(display, RED, (*self.position, GRID_SIZE, GRID_SIZE))