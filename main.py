import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20

# -- colors---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Multiplayer")
clock = pygame.time.Clock()

# -- directions --
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

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
    
    def draw(self):
        for segment in self.body:
            pygame.draw.rect(display, self.color, (*segment, GRID_SIZE, GRID_SIZE))

class Apple:
    def __init__(self):
        self.position = self.randomize_position()
    
    def randomize_position(self):
        return (
            random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )
    
    def draw(self):
        pygame.draw.rect(display, RED, (*self.position, GRID_SIZE, GRID_SIZE))


snake1 = Snake(GREEN, (100, 100), {pygame.K_UP: UP, pygame.K_DOWN: DOWN, pygame.K_LEFT: LEFT, pygame.K_RIGHT: RIGHT})
snake2 = Snake(BLUE, (300, 100), {pygame.K_w: UP, pygame.K_s: DOWN, pygame.K_a: LEFT, pygame.K_d: RIGHT})

apple = Apple()

#--game logic---
running = True
while running:
    display.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake1.change_direction(event.key)
            snake2.change_direction(event.key)
    
    snake1.move()
    snake2.move()
    
    if snake1.body[0] == apple.position:
        snake1.grow_snake()
        apple.position = apple.randomize_position()
    elif snake2.body[0] == apple.position:
        snake2.grow_snake()
        apple.position = apple.randomize_position()
    
    if snake1.check_collision() or snake2.check_collision():
        running = False
    
    snake1.draw()
    snake2.draw()
    apple.draw()
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
