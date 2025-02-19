import pygame
from settings import GRID_SIZE, WIDTH, HEIGHT

class Snake:
    def __init__(self, color, start_pos, controls):
        self.body = [list(start_pos)]
        self.direction = None
        self.grow = False
        self.color = color
        self.controls = controls
        self.can_move=False
    
    def move(self):
        if not self.can_move or self.direction is None:
            return
        
        if not self.grow and len(self.body) > 1:
            self.body.pop()
        else:
            self.grow=False
        
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        self.body.insert(0, new_head)
    
    def change_direction(self, key):
        if key in self.controls:
            new_direction = self.controls[key]
            if self.direction is None or (new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]):
                self.direction = new_direction
                self.can_move=True
    
    def check_collision(self):
        x, y = self.body[0]
        return (
            x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or
            self.body[0] in self.body[1:]
        )
    
    def grow_snake(self):
        self.grow = True
    
    def draw(self,display):
        for segment in self.body:
            pygame.draw.rect(display, self.color, (*segment, GRID_SIZE, GRID_SIZE))