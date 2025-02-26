import pygame
import math
from utils.constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, is_enemy=False):
        super().__init__()
        self.direction = direction
        self.speed = BULLET_SPEED
        self.is_enemy = is_enemy
        self.colors = BULLET_COLORS["ENEMY"] if is_enemy else BULLET_COLORS["PLAYER"]
        
        # Pré-rendu de l'effet de projectile
        self.image = pygame.Surface((BULLET_SURFACE_SIZE, BULLET_SURFACE_SIZE), pygame.SRCALPHA)
        center = BULLET_SURFACE_SIZE // 2
        
        # Effet de lueur optimisé
        pygame.draw.circle(self.image, self.colors["GLOW"], (center, center), BULLET_SIZE * 2)
        pygame.draw.circle(self.image, self.colors["CORE"], (center, center), BULLET_SIZE)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.trail_positions = []
        self.frame_count = 0

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Mise à jour de la traînée moins fréquente
        self.frame_count = (self.frame_count + 1) % TRAIL_UPDATE_FREQUENCY
        if self.frame_count == 0:
            self.trail_positions.insert(0, self.rect.center)
            if len(self.trail_positions) > MAX_TRAIL_LENGTH:
                self.trail_positions.pop()

    def draw(self, screen):
        # Dessin optimisé de la traînée
        for i, pos in enumerate(self.trail_positions):
            alpha = 255 * (1 - i/MAX_TRAIL_LENGTH)
            size = BULLET_SIZE * (1 - i/MAX_TRAIL_LENGTH)
            if size > 1:  # Évite de dessiner des cercles trop petits
                pygame.draw.circle(screen, (*self.colors["TRAIL"][:3], int(alpha)), 
                                 pos, int(size))
        
        screen.blit(self.image, self.rect)

class Weapon:
    def __init__(self):
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.cooldown = 250  # Milliseconds
        
    def shoot(self, pos, target):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.cooldown:
            direction = pygame.math.Vector2(target[0] - pos[0], target[1] - pos[1])
            if direction.length() > 0:
                direction = direction.normalize()
                bullet = Bullet(pos[0], pos[1], direction)
                self.bullets.add(bullet)
                self.last_shot = current_time