import random
import pygame
from settings import GRID_SIZE, RED

class Apple:
    def __init__(self):
        self.width = 800 
        self.height = 600 
        self.positions = []
        self.spawn_timer=0
        self.spawn_interval=1000
        self.max_apples=5
        self.last_spawn_time=0 
        
    def randomize_position(self):
        margin = 2
        max_x = (self.width // GRID_SIZE) - margin
        max_y = (self.height // GRID_SIZE) - margin
        
        x = random.randint(margin, max_x) * GRID_SIZE
        y = random.randint(margin, max_y) * GRID_SIZE
        
        return (x, y)
    
    def add_apple(self,position=None):
        if position is None:
            position=self.randomize_position()
        
        if len(self.positions) <self.max_apples:
            self.positions.append(position)
        return position
    
    def remove_apple(self,position):
        if position in self.positions:
            self.positions.remove(position)
    
    def update(self,current_time):
        if not self.positions:
            self.add_apple()
            self.last_spawn_time=current_time
            return
        
        if current_time - self.last_spawn_time >= self.spawn_interval and len(self.positions) < self.max_apples:
            self.add_apple()
            self.last_spawn_time=current_time

            self.spawn_interval=max(2000,self.spawn_interval-500)
        
    def draw(self, display):
        for position in self.positions:
            pygame.draw.rect(display, RED, (position[0], position[1], GRID_SIZE, GRID_SIZE))