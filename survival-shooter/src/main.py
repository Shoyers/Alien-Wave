import pygame
import sys
import random
import os
import math
import json
from utils.constants import *
from game.player import Player
from game.enemy import Enemy, ShootingEnemy
from utils.sound_generator import SoundGenerator
from ui.menu_manager import MenuManager

def check_assets():
    print("Vérification des assets:")
    print(f"Dossier de travail actuel: {os.getcwd()}")
    print(f"Le fichier existe: {os.path.exists(FIREBALL_SPRITE)}")
    print(f"Chemin complet: {os.path.abspath(FIREBALL_SPRITE)}")

def check_sounds():
    print("Vérification des fichiers sons:")
    sound_files = [
        SHOOT_SOUND,
        ENEMY_SHOOT_SOUND,
        HIT_SOUND,
        ENEMY_DEATH_SOUND,
        PLAYER_HURT_SOUND,
        GAME_MUSIC
    ]
    for sound_file in sound_files:
        print(f"Fichier {sound_file} existe: {os.path.exists(sound_file)}")

check_assets()
check_sounds()

class Game:
    def __init__(self):
        # Initialisation de Pygame et du mixer avec plus de canaux
        pygame.init()
        pygame.mixer.quit()  # Réinitialiser le mixer
        pygame.mixer.init(44100, -16, 2, 1024)  # Augmentation du buffer
        pygame.mixer.set_num_channels(64)  # Réduction du nombre de canaux
        
        # Configuration de l'écran
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SHOOTER SURVIVAL")
        
        # Chargement du logo avec gestion d'erreur
        try:
            self.icon = pygame.image.load(GAME_LOGO)
            pygame.display.set_icon(self.icon)  # Ajout de cette ligne pour définir l'icône
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")
        
        self.clock = pygame.time.Clock()
        
        # Initialisation des polices
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # État du jeu
        self.game_state = MENU  # État initial sur le menu
        
        self.wave_enemies_left = ENEMIES_PER_WAVE
        self.enemies_killed = 0
        self.wave_transition = False
        self.wave_start_time = 0
        
        # Génération des sons s'ils n'existent pas
        sound_gen = SoundGenerator()
        sound_gen.generate_all_sounds(SOUND_DIR)
        
        # Chargement des sons
        try:
            self.shoot_sound = pygame.mixer.Sound(SHOOT_SOUND)
            self.enemy_shoot_sound = pygame.mixer.Sound(ENEMY_SHOOT_SOUND)
            self.hit_sound = pygame.mixer.Sound(HIT_SOUND)
            self.enemy_death_sound = pygame.mixer.Sound(ENEMY_DEATH_SOUND)
            self.player_hurt_sound = pygame.mixer.Sound(PLAYER_HURT_SOUND)
            
            # Configuration du volume et durée des sons
            for sound in [self.shoot_sound, self.enemy_shoot_sound, 
                         self.hit_sound, self.enemy_death_sound, 
                         self.player_hurt_sound]:
                sound.set_volume(0.3)
                # Réduire la durée de rétention du canal
                sound.fadeout(100)  # Fade out après 100ms
            
            # Musique de fond
            self.load_background_music()
            self.play_background_music()
        except Exception as e:
            print(f"Erreur lors du chargement des sons: {e}")
            self.shoot_sound = None
            self.enemy_shoot_sound = None
            self.hit_sound = None
            self.enemy_death_sound = None
            self.player_hurt_sound = None
        
        self.sound_muted = False
        self.reset_game()
        
        # Configuration des étoiles
        self.stars = []
        self.num_stars = 150  # Augmentation du nombre d'étoiles
        self.star_speeds = [0.3, 0.5, 0.8]  # Vitesses plus douces
        self.generate_stars()
        
        # Après l'initialisation existante
        self.highscore = self.load_highscore()
        
        self.menu_manager = MenuManager(self)
        
    def set_volume(self, volume):
        """Configure le volume pour tous les sons"""
        try:
            if hasattr(self, 'shoot_sound') and self.shoot_sound:
                self.shoot_sound.set_volume(volume)
                print(f"Volume shoot_sound réglé à {volume}")
            if hasattr(self, 'enemy_shoot_sound') and self.enemy_shoot_sound:
                self.enemy_shoot_sound.set_volume(volume)
            if hasattr(self, 'hit_sound') and self.hit_sound:
                self.hit_sound.set_volume(volume)
            if hasattr(self, 'enemy_death_sound') and self.enemy_death_sound:
                self.enemy_death_sound.set_volume(volume)
            if hasattr(self, 'player_hurt_sound') and self.player_hurt_sound:
                self.player_hurt_sound.set_volume(volume)
        except Exception as e:
            print(f"Erreur lors du réglage du volume: {e}")
        
    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player.game = self  # Passer l'instance du jeu
        self.enemies = pygame.sprite.Group()
        self.wave = 1
        self.wave_enemies_left = ENEMIES_PER_WAVE
        self.enemies_killed = 0
        self.wave_transition = False
        self.wave_transition_start = 0
        self.last_spawn = 0
        self.spawn_cooldown = 2000
        
    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn >= self.spawn_cooldown and self.wave_enemies_left > 0:
            health = 50 + (self.wave * 10)
            speed = 2 + (self.wave * 0.5)
            
            if random.random() < SHOOTER_ENEMY_CHANCE:
                enemy = ShootingEnemy(health * 1.5, speed * 0.8)
            else:
                enemy = Enemy(health, speed)
            
            enemy.game = self  # Passer l'instance du jeu avec les sons
            self.enemies.add(enemy)
            self.wave_enemies_left -= 1
            self.last_spawn = current_time
            
    def update_wave(self):
        # On change de vague uniquement si tous les ennemis prévus sont apparus ET qu'il n'y en a plus sur le terrain
        if self.wave_enemies_left <= 0 and len(self.enemies) == 0:
            if not self.wave_transition:
                self.wave_transition = True
                self.wave_start_time = pygame.time.get_ticks()
                self.wave += 1
                self.enemies_killed = 0
                # Calcul du nouveau nombre d'ennemis avec le coefficient
                self.wave_enemies_left = int(ENEMIES_PER_WAVE * (WAVE_ENEMY_MULTIPLIER ** (self.wave - 1)))
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
                        try:
                            self.player_hurt_sound.play()
                        except:
                            pass
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
                try:
                    self.player_hurt_sound.play()
                except:
                    pass
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
        
        # Affichage du meilleur score
        highscore_text = self.font.render(f"Meilleur Score: {self.highscore}", True, CYAN)
        highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(highscore_text, highscore_rect)
        
        # Bouton Restart
        restart_text = self.font.render("Appuyez sur ESPACE pour recommencer", True, CYAN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(restart_text, restart_rect)
        
        # Bouton Quitter
        quit_text = self.font.render("Appuyez sur ÉCHAP pour quitter", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        self.screen.blit(quit_text, quit_rect)
        
    def game_over(self):
        self.game_state = GAME_OVER
        self.update_highscore()
        
    def handle_game_over_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.game_state = PLAYING  # Important : définir l'état à PLAYING
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
    def draw_hud(self):
        # Affichage de la santé à gauche
        health_text = self.font.render(f"Vie: {self.player.health}", True, WHITE)
        health_rect = health_text.get_rect(topleft=(20, 20))
        self.screen.blit(health_text, health_rect)
        
        # Barre de vie
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = max(0, self.player.health / 100)
        pygame.draw.rect(self.screen, RED, (20, 50, health_bar_width, health_bar_height), 2)
        pygame.draw.rect(self.screen, RED, (20, 50, health_bar_width * health_ratio, health_bar_height))
        
        # Affichage du score actuel en haut à droite
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)
        
        # Affichage de la vague au centre
        wave_text = self.font.render(f"Vague {self.wave}", True, CYAN)
        wave_rect = wave_text.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        self.screen.blit(wave_text, wave_rect)
        
        # Affichage du meilleur score sous la vague
        highscore_text = self.font.render(f"Meilleur Score : {self.highscore}", True, CYAN)
        highscore_rect = highscore_text.get_rect(midtop=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(highscore_text, highscore_rect)
        
        # Informations sur les ennemis à droite (réorganisées)
        y_offset = 60  # Commence plus haut pour combler l'espace
        spacing = 35   # Espacement réduit entre les lignes
        
        # Nombre d'ennemis actifs
        enemies_text = self.font.render(f"Ennemis: {len(self.enemies)}", True, WHITE)
        enemies_rect = enemies_text.get_rect(topright=(SCREEN_WIDTH - 20, y_offset))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Ennemis restants à faire apparaître
        remaining_text = self.font.render(f"Restants: {self.wave_enemies_left}", True, WHITE)
        remaining_rect = remaining_text.get_rect(topright=(SCREEN_WIDTH - 20, y_offset + spacing))
        self.screen.blit(remaining_text, remaining_rect)
        
        # Bouton son en bas à droite
        button_x = SCREEN_WIDTH - SOUND_BUTTON_SIZE - SOUND_BUTTON_PADDING
        button_y = SCREEN_HEIGHT - SOUND_BUTTON_SIZE - SOUND_BUTTON_PADDING
        
        # Dessiner le cercle du bouton
        color = SOUND_ON_COLOR if not self.sound_muted else SOUND_OFF_COLOR
        pygame.draw.circle(self.screen, color, (button_x + SOUND_BUTTON_SIZE//2, button_y + SOUND_BUTTON_SIZE//2), SOUND_BUTTON_SIZE//2)
        
        # Dessiner l'icône
        if not self.sound_muted:
            # Dessiner des ondes sonores
            for i in range(3):
                radius = (i + 1) * 5
                pygame.draw.arc(self.screen, WHITE,
                              (button_x + SOUND_BUTTON_SIZE//2 - radius,
                               button_y + SOUND_BUTTON_SIZE//2 - radius,
                               radius * 2, radius * 2),
                               -math.pi/4, math.pi/4, 2)
        else:
            # Dessiner une croix
            start_x = button_x + SOUND_BUTTON_SIZE//4
            start_y = button_y + SOUND_BUTTON_SIZE//4
            end_x = button_x + SOUND_BUTTON_SIZE*3//4
            end_y = button_y + SOUND_BUTTON_SIZE*3//4
            pygame.draw.line(self.screen, WHITE, (start_x, start_y), (end_x, end_y), 2)
            pygame.draw.line(self.screen, WHITE, (start_x, end_y), (end_x, start_y), 2)
        
        # Barre de cooldown du bouclier
        shield_cooldown_width = 200
        shield_cooldown_height = 20
        current_time = pygame.time.get_ticks()
        if self.player.shield_active:
            shield_ratio = 1 - (current_time - self.player.last_shield_activation) / self.player.shield_duration
        else:
            shield_ratio = min(1, (current_time - self.player.last_shield_activation) / self.player.shield_cooldown)
        
        pygame.draw.rect(self.screen, RED, (20, 80, shield_cooldown_width, shield_cooldown_height), 2)
        pygame.draw.rect(self.screen, CYAN, (20, 80, shield_cooldown_width * shield_ratio, shield_cooldown_height))
        
        # Texte du cooldown du bouclier
        shield_text = self.font.render("Bouclier", True, WHITE)
        shield_rect = shield_text.get_rect(topleft=(20, 110))
        self.screen.blit(shield_text, shield_rect)

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
            
    def toggle_sound(self):
        self.sound_muted = not self.sound_muted
        
        # Gestion des effets sonores
        volume = 0 if self.sound_muted else 0.3
        for sound in [self.shoot_sound, self.enemy_shoot_sound, 
                     self.hit_sound, self.enemy_death_sound, 
                     self.player_hurt_sound]:
            if sound:
                sound.set_volume(volume)
        
        # Gestion de la musique de fond
        if self.sound_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            if not pygame.mixer.music.get_busy():
                self.play_background_music()

    def play_sound(self, sound_type):
        if not self.sound_muted:
            try:
                sound = None
                if sound_type == 'shoot':
                    sound = self.shoot_sound
                elif sound_type == 'enemy_shoot':
                    sound = self.enemy_shoot_sound
                elif sound_type == 'hit':
                    sound = self.hit_sound
                elif sound_type == 'enemy_death':
                    sound = self.enemy_death_sound
                elif sound_type == 'player_hurt':
                    sound = self.player_hurt_sound

                if sound:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        channel.set_volume(0.3)
                        channel.play(sound, maxtime=1000)  # Limite la durée à 1 seconde
                        print(f"Son joué: {sound_type}")
            except Exception as e:
                print(f"Erreur lors de la lecture du son {sound_type}: {e}")

    def generate_stars(self):
        """Génère les étoiles initiales"""
        for _ in range(self.num_stars):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            speed = random.choice(self.star_speeds)
            brightness = random.randint(100, 255)
            size = random.randint(1, 3)
            angle = random.uniform(0, 2 * math.pi)  # Angle aléatoire pour chaque étoile
            self.stars.append({
                'pos': [x, y],
                'speed': speed,
                'brightness': brightness,
                'size': size,
                'angle': angle  # Nouvelle propriété pour la direction
            })

    def update_stars(self):
        """Met à jour la position des étoiles avec un mouvement constant"""
        for star in self.stars:
            # Mouvement constant vers le bas avec une légère dérive
            star['pos'][1] += star['speed']
            star['pos'][0] += math.sin(star['angle']) * 0.3

            # Fait réapparaître les étoiles en haut quand elles sortent de l'écran
            if star['pos'][1] > SCREEN_HEIGHT:
                star['pos'][1] = 0
                star['pos'][0] = random.randint(0, SCREEN_WIDTH)
                star['brightness'] = random.randint(100, 255)  # Nouvelle luminosité
            
            # Garde les étoiles dans les limites horizontales
            if star['pos'][0] < 0:
                star['pos'][0] = SCREEN_WIDTH
            elif star['pos'][0] > SCREEN_WIDTH:
                star['pos'][0] = 0

    def draw_stars(self):
        """Dessine les étoiles"""
        for star in self.stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(self.screen, color, 
                             (int(star['pos'][0]), int(star['pos'][1])), 
                             star['size'])

    def load_background_music(self):
        """Charge la musique de fond"""
        try:
            pygame.mixer.music.load(GAME_MUSIC)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print(f"Erreur lors du chargement de la musique de fond: {e}")

    def play_background_music(self):
        """Joue la musique de fond en boucle"""
        try:
            pygame.mixer.music.play(-1)  # -1 pour jouer en boucle
        except Exception as e:
            print(f"Erreur lors de la lecture de la musique de fond: {e}")

    def pause_background_music(self):
        """Met en pause la musique de fond"""
        pygame.mixer.music.pause()

    def resume_background_music(self):
        """Reprend la musique de fond"""
        pygame.mixer.music.unpause()

    def stop_background_music(self):
        """Arrête la musique de fond"""
        pygame.mixer.music.stop()

    def set_background_music_volume(self, volume):
        """Règle le volume de la musique de fond"""
        pygame.mixer.music.set_volume(volume)

    def get_background_music_volume(self):
        """Retourne le volume courant de la musique de fond"""
        return pygame.mixer.music.get_volume()

    def load_highscore(self):
        try:
            if not os.path.exists(os.path.dirname(SCORE_FILE)):
                os.makedirs(os.path.dirname(SCORE_FILE))
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('highscore', 0)
            return 0
        except Exception as e:
            print(f"Erreur lors du chargement du meilleur score: {e}")
            return 0

    def save_highscore(self):
        try:
            with open(SCORE_FILE, 'w') as f:
                json.dump({'highscore': self.highscore}, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du meilleur score: {e}")

    def update_highscore(self):
        if self.player.score > self.highscore:
            self.highscore = self.player.score
            self.save_highscore()

    def draw_menu(self):
        # Fond sombre semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Titre du jeu
        title_text = self.big_font.render("SHOOTER SURVIVAL", True, CYAN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        # Instructions
        start_text = self.font.render("Appuyez sur ESPACE pour commencer", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        # Meilleur score
        highscore_text = self.font.render(f"Meilleur score : {self.highscore}", True, WHITE)
        highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(highscore_text, highscore_rect)

    def draw_pause(self):
        # Fond sombre semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Texte de pause
        pause_text = self.big_font.render("PAUSE", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = self.font.render("Appuyez sur ECHAP pour reprendre", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.screen.blit(resume_text, resume_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.toggle_sound()
                    elif event.key == pygame.K_ESCAPE:
                        if self.game_state == PLAYING:
                            self.game_state = PAUSED
                        elif self.game_state == PAUSED:
                            self.game_state = PLAYING
                    elif event.key == pygame.K_SPACE:
                        if self.game_state == MENU:
                            self.reset_game()
                            self.game_state = PLAYING
                        elif self.game_state == GAME_OVER:
                            self.reset_game()
                            self.game_state = PLAYING
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_x, mouse_y = event.pos
                        button_x = SCREEN_WIDTH - SOUND_BUTTON_SIZE - SOUND_BUTTON_PADDING
                        button_y = SCREEN_HEIGHT - SOUND_BUTTON_SIZE - SOUND_BUTTON_PADDING
                        if (button_x <= mouse_x <= button_x + SOUND_BUTTON_SIZE and 
                            button_y <= mouse_y <= button_y + SOUND_BUTTON_SIZE):
                            self.toggle_sound()
                    elif event.button == 3:  # Clic droit
                        if self.game_state == PLAYING:
                            self.player.activate_shield()
            
            # Fond étoilé toujours actif
            self.screen.fill((5, 5, 15))
            self.update_stars()
            self.draw_stars()
            
            if self.game_state == MENU:
                self.menu_manager.draw_main_menu()
            elif self.game_state == PLAYING:
                self.player.update()
                if not self.wave_transition:
                    self.spawn_enemy()
                    self.update_enemies()
                self.update_effects()
                self.update_wave()
                
                self.player.draw(self.screen)
                for enemy in self.enemies:
                    enemy.draw(self.screen)
                for enemy in self.enemies:
                    if isinstance(enemy, ShootingEnemy):
                        enemy.bullets.draw(self.screen)
                self.draw_hud()
                self.draw_wave_transition()
            elif self.game_state == PAUSED:
                self.menu_manager.draw_pause_menu()
            elif self.game_state == GAME_OVER:
                self.menu_manager.draw_game_over_menu()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()