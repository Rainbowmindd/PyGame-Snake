import pygame
from settings import WIDTH, HEIGHT, BLACK, WHITE,RED

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        
    def draw_button(self, display, text, position, selected=False):
        color = RED if selected else WHITE
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        display.blit(text_surface, text_rect)
        return text_rect
        
    def draw_main_menu(self, display, selected_option):
        display.fill(BLACK)
        
        title = self.font.render("Snake Multiplayer", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        display.blit(title, title_rect)
        
        options = ["New Game", "High Scores", "Exit"]
        buttons = []
        
        for i, option in enumerate(options):
            btn_rect = self.draw_button(
                display,
                option,
                (WIDTH//2, HEIGHT//2 + i * 50),
                i == selected_option
            )
            buttons.append((btn_rect, option))
            
        pygame.display.flip()
        return buttons

    def draw_scores(self, display, scoreboard, selected_option):
        display.fill(BLACK)
        
        title = self.font.render("High Scores", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        display.blit(title, title_rect)
        
        y = 100
        for score in scoreboard.highscores[:10]:
            score_text = f"{score['winner']}: {max(score['player1']['score'], score['player2']['score'])}"
            text_surface = self.font.render(score_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH//2, y))
            display.blit(text_surface, text_rect)
            y += 30
            
        back_btn = self.draw_button(
            display,
            "Back to Menu",
            (WIDTH//2, HEIGHT - 50),
            selected_option == 0
        )
        
        pygame.display.flip()
        return [(back_btn, "Back")]
