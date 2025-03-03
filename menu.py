import pygame
import time
from settings import BLACK, WHITE, RED


pygame.font.init()
FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"  
FONT_SIZE = 24

class Menu:
    def __init__(self):
        self.large_font = pygame.font.Font(FONT_PATH, FONT_SIZE+30)
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.width = 800  
        self.height = 600 
        self.title_alpha = 255 
        self.title_fade_direction = -5
    
    def update_screen_size(self, width, height):
        self.width = width
        self.height = height
    
    def draw_button(self, display, text, position, selected=False):
        color = RED if selected else WHITE
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        
   
        offset = -5 if selected else 0
        text_rect.y += offset
        
  
        border_rect = text_rect.inflate(10, 10)
        pygame.draw.rect(display, WHITE, border_rect, 3)  
        pygame.draw.rect(display, BLACK, text_rect) 
        
        display.blit(text_surface, text_rect)
        return text_rect
    
    def draw_main_menu(self, display, selected_option):
        display.fill(BLACK)

 
        title = self.large_font.render("Snake Multiplayer", True, (WHITE[0], WHITE[1], WHITE[2], self.title_alpha))
        title_rect = title.get_rect(center=(self.width//2, self.height//4))
        display.blit(title, title_rect)
        

        self.title_alpha += self.title_fade_direction
        if self.title_alpha <= 100 or self.title_alpha >= 255:
            self.title_fade_direction *= -1
        
        options = ["New Game", "High Scores", "Exit"]
        buttons = []
        
        for i, option in enumerate(options):
            btn_rect = self.draw_button(
                display,
                option,
                (self.width//2, self.height//2 + i * 60),
                i == selected_option
            )
            buttons.append((btn_rect, option))
            
        pygame.display.flip()
        return buttons
    
    def draw_scores(self, display, scoreboard, selected_option):
        display.fill(BLACK)
        
        title = self.font.render("High Scores", True, WHITE)
        title_rect = title.get_rect(center=(self.width//2, 50))
        display.blit(title, title_rect)
        
        y = 100
        for score in scoreboard.highscores[:10]:
            score_text = f"{score['winner']}: {max(score['player1']['score'], score['player2']['score'])}"
            text_surface = self.font.render(score_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width//2, y))
            display.blit(text_surface, text_rect)
            y += 40
        
        back_btn = self.draw_button(
            display,
            "Back to Menu",
            (self.width//2, self.height - 50),
            selected_option == 0
        )
        
        pygame.display.flip()
        return [(back_btn, "Back")]
