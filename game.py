import pygame
from settings import (BLACK, GREEN, BLUE, UP, DOWN, LEFT, RIGHT, WHITE, MAX_ROUNDS, 
                      POINTS_PER_APPLE, GRID_SIZE)

from snake import Snake
from apple import Apple
from scoreboard import Scoreboard
from menu import Menu,FONT_PATH, FONT_SIZE

class Game:
    def __init__(self):
        pygame.init()

        screen_info = pygame.display.Info()
        self.WIDTH = screen_info.current_w
        self.HEIGHT = screen_info.current_h
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Snake Multiplayer")
        self.GRID_SIZE = GRID_SIZE
        self.GRID_WIDTH = self.WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.GRID_SIZE
        self.clock = pygame.time.Clock()
        self.font=pygame.font.Font(FONT_PATH, FONT_SIZE)

        self.player1_name = None
        self.player2_name = None

        self.state = "name_input"
        self.current_player = 1
        self.name_input = ""

        self.snake1 = None
        self.snake2 = None

        self.apple = Apple()
        self.apple.width = self.WIDTH
        self.apple.height = self.HEIGHT
        
        self.scoreboard = Scoreboard()
        self.menu = Menu()
  
        self.menu.width = self.WIDTH
        self.menu.height = self.HEIGHT
        
        self.selected_option = 0
        self.current_round = 1
        self.running = True
        self.paused = False

        self.apple_resets = 0
        
        
    def initialize_snake(self):
        self.snake1 = Snake(GREEN, ((self.GRID_WIDTH//4)*self.GRID_SIZE, (self.GRID_HEIGHT//2)*self.GRID_SIZE), {
            pygame.K_UP: UP,
            pygame.K_DOWN: DOWN,
            pygame.K_LEFT: LEFT,
            pygame.K_RIGHT: RIGHT
        }, self.player1_name,'assets/sprites/snake_sprite/orange_snake','assets/sprites/snake_sprite/blue_snake')
        
        self.snake2 = Snake(BLUE, ((3*self.GRID_WIDTH//4)*self.GRID_SIZE, (self.GRID_HEIGHT//2)*self.GRID_SIZE), {
            pygame.K_w: UP,
            pygame.K_s: DOWN,
            pygame.K_a: LEFT,
            pygame.K_d: RIGHT
        }, self.player2_name ,'assets/sprites/snake_sprite/blue_snake','assets/sprites/snake_sprite/blue_snake')

        self.snake1.width = self.WIDTH
        self.snake1.height = self.HEIGHT
        self.snake2.width = self.WIDTH
        self.snake2.height = self.HEIGHT

        self.generate_safe_apple_position()
    
    def generate_safe_apple_position(self):
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            new_pos = self.apple.randomize_position()
            if self.snake1 is None or self.snake2 is None:
                self.apple.add_apple(new_pos)
                return
                

            snake1_body = [tuple(pos) if isinstance(pos, list) else pos for pos in self.snake1.body]
            snake2_body = [tuple(pos) if isinstance(pos, list) else pos for pos in self.snake2.body]
            
   
            if new_pos not in snake1_body and new_pos not in snake2_body:
                self.apple.add_apple(new_pos)
                return
                
            attempts += 1

        default_pos = ((self.GRID_WIDTH // 2) * self.GRID_SIZE, 
                              (self.GRID_HEIGHT // 2) * self.GRID_SIZE)
        self.apple.position = default_pos
    
    def reset_round(self):
        self.snake1.reset(((self.GRID_WIDTH // 4) * self.GRID_SIZE, (self.GRID_HEIGHT // 2) * self.GRID_SIZE))
        self.snake2.reset(((3 * self.GRID_WIDTH // 4) * self.GRID_SIZE, (self.GRID_HEIGHT // 2) * self.GRID_SIZE))
        
        self.apple.positions=[]
        self.apple.spawn_interval=1000
        self.apple.last_spawn_time=0
        self.apple.last_spawn_time=pygame.time.get_ticks()

        self.generate_safe_apple_position()

    def handle_name_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(self.name_input) > 0:
                    if self.current_player == 1:
                        self.player1_name = self.name_input
                        self.name_input = ""
                        self.current_player = 2
                    else:
                        self.player2_name = self.name_input
                        self.initialize_snake()
                        self.state = "menu"
                        self.name_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.name_input = self.name_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.running = False 
                elif event.unicode.isalnum() or event.unicode.isspace():
                    if len(self.name_input) < 15:  
                        self.name_input += event.unicode

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
                elif event.key == pygame.K_ESCAPE:
                    if self.state == "scores":
                        self.state = "menu"
                        self.selected_option = 0
                    else:
                        self.running = False
    
    def handle_game_events(self):
        if self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        self.paused = False
                    elif event.key == pygame.K_ESCAPE: 
                        self.state = "menu"
                        self.paused = False
                    else:
                        self.paused = True
            return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.snake1.change_direction(event.key)
                    self.snake2.change_direction(event.key)
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                    elif event.key == pygame.K_p:
                        self.paused = True

                
    def check_snake_collision(self, snake):
        head_x, head_y = snake.body[0]
        
        #wall collision
        if (head_x < 0 or head_x >= self.WIDTH or 
            head_y < 0 or head_y >= self.HEIGHT):
            return True
            
        #self collision
        head_pos = tuple(snake.body[0]) if isinstance(snake.body[0], list) else snake.body[0]
        for segment in snake.body[1:]:
            segment_pos = tuple(segment) if isinstance(segment, list) else segment
            if head_pos == segment_pos:
                return True
                
        return False
                
    def update(self):

        current_time=pygame.time.get_ticks()

        self.apple.update(current_time)
      
        self.snake1.move()
        self.snake2.move()
        
     
        snake1_head = tuple(self.snake1.body[0]) if isinstance(self.snake1.body[0], list) else self.snake1.body[0]
        snake2_head = tuple(self.snake2.body[0]) if isinstance(self.snake2.body[0], list) else self.snake2.body[0]
        #apple_pos = self.apple.position
        
        #apple collision
        for apple_pos in self.apple.positions[:]:
            if snake1_head == apple_pos:
                self.snake1.grow_snake()
                self.snake1.add_points(POINTS_PER_APPLE)
                self.apple.remove_apple(apple_pos)
                self.generate_safe_apple_position()
                self.apple_resets += 1
                    
            elif snake2_head == apple_pos:
                self.snake2.grow_snake()
                self.snake2.add_points(POINTS_PER_APPLE)
                self.apple.remove_apple(apple_pos)
                self.generate_safe_apple_position()
                self.apple_resets += 1
            
        #wall or self collision
        snake1_collision = self.check_snake_collision(self.snake1)
        snake2_collision = self.check_snake_collision(self.snake2)
        
        #players collision
        for segment in self.snake2.body:
            if snake1_head == (tuple(segment) if isinstance(segment, list) else segment):
                snake1_collision = True
                break
                
        for segment in self.snake1.body:
            if snake2_head == (tuple(segment) if isinstance(segment, list) else segment):
                snake2_collision = True
                break
        

        if snake1_collision or snake2_collision:
            if self.current_round < MAX_ROUNDS:
                self.current_round += 1
                self.reset_round()
            else:
                self.scoreboard.add_game_result(self.snake1, self.snake2)
                self.state = "menu"
            
    def draw_game(self):
        self.display.fill(BLACK)
        
        score1 = self.font.render(f"{self.snake1.player_name}: {self.snake1.score}", True, WHITE)
        score2 = self.font.render(f"{self.snake2.player_name}: {self.snake2.score}", True, WHITE)
        round_text = self.font.render(f"Round {self.current_round}/{MAX_ROUNDS}", True, WHITE)
        
        self.display.blit(score1, (self.WIDTH // 4, 10)) 
        self.display.blit(score2, ((3 * self.WIDTH) // 4 - score2.get_width(), 10)) 
        self.display.blit(round_text, (self.WIDTH // 2 - round_text.get_width() // 2, 10))  
        
        
        self.snake1.draw(self.display)
        self.snake2.draw(self.display)
        self.apple.draw(self.display)
        
        pygame.display.flip()
        
    def draw_name_input(self):
        self.display.fill(BLACK)
    
        prompt = f"ENTER PLAYER'S NAME {self.current_player}:"
        prompt_surface = self.font.render(prompt, True, WHITE)
        prompt_rect = prompt_surface.get_rect(center=(self.WIDTH//2, self.HEIGHT//3))
        self.display.blit(prompt_surface, prompt_rect)
    
        
        input_text = self.name_input
        if pygame.time.get_ticks() % 1000 < 500:  
            input_text += "|"
        input_surface = self.font.render(input_text, True, WHITE)
        input_rect = input_surface.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
        self.display.blit(input_surface, input_rect)
    
        instructions = [
            "ENTER - CONFIRM",
            "BACKSPACE - DELETE",
            "ESC - EXIT GAME"
        ]
    
        small_font = pygame.font.Font(FONT_PATH, FONT_SIZE - 10)
        for i, instruction in enumerate(instructions):
            inst_surface = small_font.render(instruction, True, WHITE)
            inst_rect = inst_surface.get_rect(center=(self.WIDTH//2, 2*self.HEIGHT//3 + i*40))
            self.display.blit(inst_surface, inst_rect)
    
        pygame.display.flip()
    def draw_pause_screen(self):
        self.display.fill(BLACK)

        large_font = pygame.font.Font(FONT_PATH, FONT_SIZE + 20)
        pause_text = large_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 3))
        self.display.blit(pause_text, pause_rect)

        instructions = [
            "Press ENTER to resume",
            "Press ESC to return to the menu"
        ]
 
        small_font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        for i, instruction in enumerate(instructions):
            inst_surface = small_font.render(instruction, True, WHITE)
            inst_rect = inst_surface.get_rect(center=(self.WIDTH // 2, 2 * self.HEIGHT // 3 + i * 40))
            self.display.blit(inst_surface, inst_rect)

        pygame.display.flip()
    
    def run(self):
        while self.running:
            if self.paused:
                self.draw_pause_screen()
                self.handle_game_events()
            else:
                if self.state == "name_input":
                    self.draw_name_input()
                    self.handle_name_input()
                elif self.state == "menu":
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