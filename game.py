import pygame
from settings import WIDTH,HEIGHT,BLACK,GREEN,BLUE,UP,DOWN,LEFT,RIGHT
from snake import Snake
from apple import Apple

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Multiplayer")
        self.clock = pygame.time.Clock()
        
        self.snake1 = Snake(GREEN, (100, 100), {
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT
        })
        
        self.snake2 = Snake(BLUE, (300, 100), {
            pygame.K_w: UP,
            pygame.K_s: DOWN,
            pygame.K_a: LEFT,
            pygame.K_d: RIGHT
        })
        
        self.apple = Apple()
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.snake1.change_direction(event.key)
                self.snake2.change_direction(event.key)
                
    def update(self):
        self.snake1.move()
        self.snake2.move()
        
        if self.snake1.body[0] == self.apple.position:
            self.snake1.grow_snake()
            self.apple.position = self.apple.randomize_position()
        elif self.snake2.body[0] == self.apple.position:
            self.snake2.grow_snake()
            self.apple.position = self.apple.randomize_position()
            
        if self.snake1.check_collision() or self.snake2.check_collision():
            self.running = False
            
    def draw(self):
        self.display.fill(BLACK)
        self.snake1.draw(self.display)
        self.snake2.draw(self.display)
        self.apple.draw(self.display)
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)
        pygame.quit()