from utils.constants import *
import pygame

class MenuManager:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = game.font
        self.big_font = game.big_font
        
    def draw_main_menu(self):
        self._draw_overlay()
        self._draw_title("ALIEN WAVE", CYAN)
        self._draw_text("Appuyez sur ESPACE pour commencer", WHITE, 0.5)
        self._draw_text(f"Meilleur score : {self.game.highscore}", WHITE, 0.66)
    
    def draw_pause_menu(self):
        self._draw_overlay()
        self._draw_title("PAUSE", WHITE)
        self._draw_text("Appuyez sur ECHAP pour reprendre", WHITE, 0.66)
    
    def draw_settings_menu(self):
        self._draw_overlay()
        self._draw_title("PARAMÈTRES", WHITE)
        self._draw_resolution_buttons()
        self._draw_back_button()
    
    def draw_game_over_menu(self):
        self._draw_overlay()
        self._draw_title("GAME OVER", RED)
        self._draw_text(f"Score Final: {self.game.player.score}", WHITE, 0.5)
        self._draw_text(f"Meilleur Score: {self.game.highscore}", CYAN, 0.58)
        self._draw_text("Appuyez sur ESPACE pour recommencer", CYAN, 0.66)
        self._draw_text("Appuyez sur ÉCHAP pour quitter", WHITE, 0.75)
    
    def _draw_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
    
    def _draw_title(self, text, color):
        title_text = self.big_font.render(text, True, color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
    
    def _draw_text(self, text, color, y_ratio):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * y_ratio))
        self.screen.blit(text_surface, text_rect)
    
    def _draw_settings_button(self):
        settings_text = self.font.render("Paramètres", True, WHITE)
        self.settings_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.75))
        pygame.draw.rect(self.screen, WHITE, self.settings_rect.inflate(20, 10), 1)
        self.screen.blit(settings_text, self.settings_rect) 