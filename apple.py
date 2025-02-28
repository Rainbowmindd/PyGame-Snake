import random
import pygame
from settings import GRID_SIZE, RED

class Apple:
    def __init__(self):
        self.width = 800 
        self.height = 600 
        self.position = (0, 0)  
        
    def randomize_position(self):
        margin = 2
        max_x = (self.width // GRID_SIZE) - margin
        max_y = (self.height // GRID_SIZE) - margin
        
        x = random.randint(margin, max_x) * GRID_SIZE
        y = random.randint(margin, max_y) * GRID_SIZE
        
        return (x, y)
        
    def draw(self, display):
        pygame.draw.rect(display, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))