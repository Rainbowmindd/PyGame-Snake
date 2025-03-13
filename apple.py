import random
import pygame
from settings import GRID_SIZE, RED

class Apple:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.positions = []
        self.spawn_timer = 0
        self.spawn_interval = 1000
        self.max_apples = 5
        self.last_spawn_time = 0

        self.image = pygame.image.load("assets/sprites/apple.png")
        scale_factor = 4
        self.image_original = pygame.transform.scale(
            self.image, 
            (int(GRID_SIZE * scale_factor), int(GRID_SIZE * scale_factor))
        )
        
        self.image_rect = self.image_original.get_rect()

    def randomize_position(self):
        margin = 2
        max_x = (self.width // GRID_SIZE) - margin
        max_y = (self.height // GRID_SIZE) - margin

        x = random.randint(margin, max_x) * GRID_SIZE
        y = random.randint(margin, max_y) * GRID_SIZE

        return (x, y)

    def add_apple(self, position=None):
        if position is None:
            position = self.randomize_position()

        if len(self.positions) < self.max_apples:
            self.positions.append(position)
        return position

    def remove_apple(self, position):
        if position in self.positions:
            self.positions.remove(position)

    def update(self, current_time):
        if not self.positions:
            self.add_apple()
            self.last_spawn_time = current_time
            return

        if current_time - self.last_spawn_time >= self.spawn_interval and len(self.positions) < self.max_apples:
            self.add_apple()
            self.last_spawn_time = current_time

        # Gradually decrease spawn interval, but not below 2000 ms
        self.spawn_interval = max(2000, self.spawn_interval - 500)

    def draw(self, display):
        for position in self.positions:
            apple_rect = self.image_rect.copy()
            apple_rect.topleft = position
      
            offset_x = (GRID_SIZE - apple_rect.width) // 2
            offset_y = (GRID_SIZE - apple_rect.height) // 2
            apple_rect.topleft = (position[0] + offset_x, position[1] + offset_y)
            
            display.blit(self.image_original, apple_rect)