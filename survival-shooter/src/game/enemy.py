import pygame
import math
import random
from utils.constants import *
from game.weapon import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, speed):
        super().__init__()
        self.health = health
        self.speed = speed
        
        # Chargement et redimensionnement du sprite
        try:
            self.image = pygame.image.load(ENEMY_SPRITE).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        except:
            # Fallback au dessin par défaut si le sprite n'est pas trouvé
            self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE), pygame.SRCALPHA)
            center = ENEMY_SIZE // 2
            points = []
            for i in range(8):
                angle = i * (2 * math.pi / 8)
                radius = ENEMY_SIZE//2 if i % 2 == 0 else ENEMY_SIZE//3
                points.append((
                    center + radius * math.cos(angle),
                    center + radius * math.sin(angle)
                ))
            pygame.draw.polygon(self.image, (*ENEMY_COLOR, 128), points)
            scaled_points = [(center + (x-center)*0.7, center + (y-center)*0.7) for x, y in points]
            pygame.draw.polygon(self.image, ENEMY_COLOR, scaled_points)
        
        self.rect = self.image.get_rect()
        self.spawn()
        
    def spawn(self):
        # Spawn l'ennemi sur un des bords de l'écran aléatoirement
        side = random.randint(0, 3)
        if side == 0:  # Haut
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = -ENEMY_SIZE
        elif side == 1:  # Droite
            self.rect.x = SCREEN_WIDTH + ENEMY_SIZE
            self.rect.y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bas
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = SCREEN_HEIGHT + ENEMY_SIZE
        else:  # Gauche
            self.rect.x = -ENEMY_SIZE
            self.rect.y = random.randint(0, SCREEN_HEIGHT)

    def move(self, target_position):
        # Calcul du vecteur de direction vers le joueur
        dx = target_position[0] - self.rect.centerx
        dy = target_position[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance != 0:
            # Normalisation et application de la vitesse
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            
            # Mise à jour de la position
            self.rect.x += dx
            self.rect.y += dy

    def attack(self, player):
        # Vérifie si l'ennemi touche le joueur
        if self.rect.colliderect(player.rect):
            player.take_damage(ENEMY_DAMAGE)
            return True
        return False

    def play_sound(self, sound_type):
        if hasattr(self, 'game') and not self.game.sound_muted:
            try:
                if sound_type == 'shoot' and self.game.enemy_shoot_sound:
                    pygame.mixer.find_channel(True).play(self.game.enemy_shoot_sound)
                elif sound_type == 'death' and self.game.enemy_death_sound:
                    pygame.mixer.find_channel(True).play(self.game.enemy_death_sound)
                elif sound_type == 'hit' and self.game.hit_sound:
                    pygame.mixer.find_channel(True).play(self.game.hit_sound)
            except Exception as e:
                print(f"Enemy sound error ({sound_type}): {e}")

    def die(self):
        self.play_sound('death')
        self.kill()
        return ENEMY_SCORE

    def take_damage(self, amount):
        self.health -= amount
        self.play_sound('hit')
        if self.health <= 0:
            return self.die()
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ShootingEnemy(Enemy):
    def __init__(self, health, speed):
        super().__init__(health, speed)
        self.last_shot = 0
        self.shoot_cooldown = 2000
        self.bullets = pygame.sprite.Group()
        
        # Chargement du sprite spécifique
        try:
            self.image = pygame.image.load(SHOOTER_ENEMY_SPRITE).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        except:
            # Fallback au dessin par défaut
            self.image.fill((0, 0, 0, 0))
            center = ENEMY_SIZE // 2
            points = []
            for i in range(5):
                angle = i * (2 * math.pi / 5) - math.pi/2
                points.append((
                    center + ENEMY_SIZE/2 * math.cos(angle),
                    center + ENEMY_SIZE/2 * math.sin(angle)
                ))
            pygame.draw.polygon(self.image, (*SHOOTER_ENEMY_COLOR, 128), points)
            scaled_points = [(center + (x-center)*0.7, center + (y-center)*0.7) for x, y in points]
            pygame.draw.polygon(self.image, SHOOTER_ENEMY_COLOR, scaled_points)
        
    def update(self, player_pos):
        super().move(player_pos)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_cooldown:
            self.shoot(player_pos)
            
    def shoot(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            direction = (dx/distance, dy/distance)
            bullet = Bullet(self.rect.centerx, self.rect.centery, direction, is_enemy=True)
            self.bullets.add(bullet)
            if hasattr(self, 'game') and self.game.enemy_shoot_sound and not self.game.sound_muted:
                self.game.enemy_shoot_sound.play()
            self.last_shot = pygame.time.get_ticks()