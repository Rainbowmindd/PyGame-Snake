import pygame
from settings import GRID_SIZE
import os

class Snake:
    def __init__(self, color, start_pos, controls, player_name, head_sprites_folder):
        self.body = [start_pos]  
        self.direction = None
        self.grow = False
        self.color = color
        self.controls = controls
        self.can_move = False
        self.score = 0
        self.player_name = player_name
        self.width = 800  
        self.height = 600  

        self.head_sprites = {}
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            try:
                sprite_path = os.path.join(head_sprites_folder, f'head_{direction}40.png')
                sprite = pygame.image.load(sprite_path).convert_alpha()
                scaled_size = int(GRID_SIZE * 2)
                sprite = pygame.transform.scale(sprite, (scaled_size, scaled_size))
                self.head_sprites[direction] = sprite
            except Exception as e:
                print(f"Error loading {direction} head sprite: {e}")
        
    def reset(self, start_pos):
        self.body = [start_pos]  
        self.direction = None
        self.grow = False
        self.can_move = False
        
    def move(self):
        if not self.can_move or self.direction is None:
            return
        
        if not self.grow and len(self.body) > 1:
            self.body.pop()  
        else:
            self.grow = False  
            
     
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
     
        self.body.insert(0, new_head)
        
    def change_direction(self, key):
        if key in self.controls:
            new_direction = self.controls[key]
            
            #180 turn prevention
            if self.direction is None or (new_direction[0] != -self.direction[0] or new_direction[1] != -self.direction[1]):
                self.direction = new_direction
                self.can_move = True
                
    def check_collision(self):
        if not self.body: 
            return False
            
        head_x, head_y = self.body[0]
        
        #wall collision
        if head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height:
            return True
            
        #self collision
        for segment in self.body[1:]:
            if self.body[0] == segment:
                return True
                
        return False
        
    def grow_snake(self):
        self.grow = True
        
    def add_points(self, points):
        self.score += points
        
    def draw(self, display):
        for i, segment in enumerate(self.body):
            if i == 0 and self.direction:
                scaled_size = int(GRID_SIZE * 2)
                offset = (scaled_size - GRID_SIZE) // 2

                if self.direction == (0, -GRID_SIZE):  
                    head_sprite = self.head_sprites.get('up')
                elif self.direction == (0, GRID_SIZE):  
                    head_sprite = self.head_sprites.get('down')
                elif self.direction == (-GRID_SIZE, 0):  
                    head_sprite = self.head_sprites.get('left')
                elif self.direction == (GRID_SIZE, 0):  
                    head_sprite = self.head_sprites.get('right')
                else:
                    head_sprite = None
                
                if head_sprite:
                    display.blit(head_sprite, (segment[0] - offset, segment[1] - offset))
                else:
                    pygame.draw.rect(display, self.color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            else:
                pygame.draw.rect(display, self.color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))