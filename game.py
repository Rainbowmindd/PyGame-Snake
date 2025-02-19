import pygame
from settings import (WIDTH,HEIGHT,BLACK,GREEN,BLUE,UP,DOWN,LEFT,RIGHT,WHITE,MAX_ROUNDS,POINTS_PER_APPLE)
from snake import Snake
from apple import Apple
from scoreboard import Scoreboard
from menu import Menu

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
        },"Player 1")
        
        self.snake2 = Snake(BLUE, (300, 100), {
            pygame.K_w: UP,
            pygame.K_s: DOWN,
            pygame.K_a: LEFT,
            pygame.K_d: RIGHT
        },"Player 2")
        
        self.state="menu"
        self.apple = Apple()
        self.scoreboard = Scoreboard()
        self.menu = Menu()
        self.selected_option = 0
        self.current_round=1
        self.running = True
    
    def reset_round(self):
        self.snake1.reset((100, 100))
        self.snake2.reset((300, 100))
        self.apple.position = self.apple.randomize_position()

    def handle_menu_input(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    _, option = buttons[self.selected_option]
                    if option == "New Game":
                        self.state = "game"
                        self.current_round = 1
                        self.snake1.score = 0
                        self.snake2.score = 0
                        self.reset_round()
                    elif option == "High Scores":
                        self.state = "scores"
                        self.selected_option = 0
                    elif option == "Exit":
                        self.running = False
                    elif option == "Back":
                        self.state = "menu"
                        self.selected_option = 0   
    def handle_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.snake1.change_direction(event.key)
                self.snake2.change_direction(event.key)
                if event.key==pygame.K_ESCAPE:
                    self.state="menu"
                
    def update(self):
        self.snake1.move()
        self.snake2.move()
        
        if self.snake1.body[0] == self.apple.position:
            self.snake1.grow_snake()
            self.snake1.add_points(POINTS_PER_APPLE)
            self.apple.position = self.apple.randomize_position()
        elif self.snake2.body[0] == self.apple.position:
            self.snake2.grow_snake()
            self.snake2.add_points(POINTS_PER_APPLE)
            self.apple.position = self.apple.randomize_position()
            
        if self.snake1.check_collision() or self.snake2.check_collision():
            if self.current_round<MAX_ROUNDS:
                self.current_round+=1
                self.reset_round()
            else:
                self.scoreboard.add_game_result(self.snake1,self.snake2)
                self.state="menu"
            
    def draw_game(self):
        self.display.fill(BLACK)
        
        # Draw scores
        font = pygame.font.Font(None, 36)
        score1 = font.render(f"{self.snake1.player_name}: {self.snake1.score}", True, WHITE)
        score2 = font.render(f"{self.snake2.player_name}: {self.snake2.score}", True, WHITE)
        round_text = font.render(f"Round {self.current_round}/{MAX_ROUNDS}", True, WHITE)
        
        self.display.blit(score1, (10, 10))
        self.display.blit(score2, (WIDTH - 150, 10))
        self.display.blit(round_text, (WIDTH//2 - 50, 10))
        
        self.snake1.draw(self.display)
        self.snake2.draw(self.display)
        self.apple.draw(self.display)
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            if self.state == "menu":
                buttons = self.menu.draw_main_menu(self.display, self.selected_option)
                self.handle_menu_input(buttons)
            elif self.state == "scores":
                buttons = self.menu.draw_scores(self.display, self.scoreboard, self.selected_option)
                self.handle_menu_input(buttons)
            elif self.state == "game":
                self.handle_game_events()
                self.update()
                self.draw_game()
            
            self.clock.tick(10)
            
        pygame.quit()