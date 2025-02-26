import pygame
import sys
import random
from utils.constants import *
from game.player import Player
from game.enemy import Enemy, ShootingEnemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("CYBER SURVIVAL")
        self.clock = pygame.time.Clock()
        self.reset_game()
        
        # Configuration des polices
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # État du jeu
        self.game_state = "playing"  # "playing" ou "game_over"
        
        self.wave_enemies_left = ENEMIES_PER_WAVE
        self.enemies_killed = 0
        self.wave_transition = False
        self.wave_start_time = 0
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = pygame.sprite.Group()
        self.last_spawn = 0
        self.spawn_cooldown = 2000
        self.wave = 1
        self.wave_enemies_left = ENEMIES_PER_WAVE
        self.enemies_killed = 0
        self.wave_transition = False
        self.game_state = "playing"
        
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn >= self.spawn_cooldown and self.wave_enemies_left > 0:
            health = 50 + (self.wave * 10)
            speed = 2 + (self.wave * 0.5)
            
            # Chance de spawner un ennemi qui tire
            if random.random() < SHOOTER_ENEMY_CHANCE:
                enemy = ShootingEnemy(health * 1.5, speed * 0.8)  # Plus résistant mais plus lent
            else:
                enemy = Enemy(health, speed)
            
            self.enemies.add(enemy)
            self.wave_enemies_left -= 1
            self.last_spawn = current_time
            
    def update_wave(self):
        if self.enemies_killed >= ENEMIES_PER_WAVE:
            if not self.wave_transition:
                self.wave_transition = True
                self.wave_start_time = pygame.time.get_ticks()
                self.wave += 1
                self.enemies_killed = 0
                self.spawn_cooldown = max(500, self.spawn_cooldown - WAVE_SPEEDUP)
                
        if self.wave_transition:
            if pygame.time.get_ticks() - self.wave_start_time > WAVE_TRANSITION_TIME:
                self.wave_transition = False
                
    def update_enemies(self):
        for enemy in self.enemies:
            if isinstance(enemy, ShootingEnemy):
                enemy.update((self.player.x, self.player.y))
                # Gestion des balles ennemies
                for bullet in enemy.bullets:
                    if bullet.rect.colliderect(self.player.rect):
                        self.player.take_damage(ENEMY_BULLET_DAMAGE)
                        bullet.kill()
                enemy.bullets.update()
            else:
                enemy.move((self.player.x, self.player.y))
            
            # Vérifie les collisions avec les balles
            bullet_hits = pygame.sprite.spritecollide(enemy, self.player.bullets, True)
            for bullet in bullet_hits:
                if enemy.take_damage(BULLET_DAMAGE):
                    self.player.gain_score(ENEMY_SCORE)
                    self.enemies_killed += 1  # Compte les ennemis tués
            
            # Vérifie les collisions avec le joueur
            if enemy.attack(self.player):
                if self.player.health <= 0:
                    self.game_over()
                    
    def draw_game_over(self):
        # Fond semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BG_COLOR)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Texte "GAME OVER"
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score final
        score_text = self.font.render(f"Score Final: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Bouton Restart
        restart_text = self.font.render("Appuyez sur ESPACE pour recommencer", True, CYAN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(restart_text, restart_rect)
        
        # Bouton Quitter
        quit_text = self.font.render("Appuyez sur ÉCHAP pour quitter", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        self.screen.blit(quit_text, quit_rect)
        
    def game_over(self):
        self.game_state = "game_over"
        
    def handle_game_over_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.reset_game()
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            
    def draw_hud(self):
        # Affichage de la santé
        health_text = self.font.render(f"Vie: {self.player.health}", True, WHITE)
        health_rect = health_text.get_rect(topleft=(20, 20))
        self.screen.blit(health_text, health_rect)
        
        # Barre de vie
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = max(0, self.player.health / 100)
        pygame.draw.rect(self.screen, RED, (20, 50, health_bar_width, health_bar_height), 2)
        pygame.draw.rect(self.screen, RED, (20, 50, health_bar_width * health_ratio, health_bar_height))
        
        # Affichage du score
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)
        
        # Affichage de la vague
        wave_text = self.font.render(f"Vague {self.wave}", True, CYAN)
        wave_rect = wave_text.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(wave_text, wave_rect)
        
        # Affichage du nombre d'ennemis
        enemies_text = self.font.render(f"Ennemis: {len(self.enemies)}", True, WHITE)
        enemies_rect = enemies_text.get_rect(topright=(SCREEN_WIDTH - 20, 60))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Affichage des ennemis restants pour la vague
        remaining_text = self.font.render(f"Restants: {self.wave_enemies_left}", True, WHITE)
        remaining_rect = remaining_text.get_rect(topright=(SCREEN_WIDTH - 20, 100))
        self.screen.blit(remaining_text, remaining_rect)
        
    def update_effects(self):
        # Mise à jour des effets visuels
        if TRAIL_EFFECT:
            self.player.trail.append((self.player.rect.center, 255))
            # Faire disparaître progressivement la traînée
            self.player.trail = [(pos, alpha-10) for pos, alpha in self.player.trail if alpha > 0]
        
    def draw_wave_transition(self):
        if self.wave_transition:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BG_COLOR)
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            wave_text = self.big_font.render(f"VAGUE {self.wave}", True, CYAN)
            wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(wave_text, wave_rect)
            
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if self.game_state == "playing":
                # Update
                self.player.update()
                if not self.wave_transition:
                    self.spawn_enemy()
                self.update_enemies()
                self.update_effects()
                self.update_wave()
                
                # Draw
                self.screen.fill(BG_COLOR)
                self.player.draw(self.screen)
                self.enemies.draw(self.screen)
                # Dessiner les balles des ennemis qui tirent
                for enemy in self.enemies:
                    if isinstance(enemy, ShootingEnemy):
                        enemy.bullets.draw(self.screen)
                self.draw_hud()
                self.draw_wave_transition()
            
            elif self.game_state == "game_over":
                self.handle_game_over_input()
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()