import pygame
from utils.constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE*2, BULLET_SIZE*2), pygame.SRCALPHA)
        
        # Effet de "boule d'énergie"
        center = BULLET_SIZE
        for radius in range(BULLET_SIZE*2, 0, -2):
            alpha = 128 if radius == BULLET_SIZE*2 else 255
            pygame.draw.circle(self.image, (*BULLET_COLOR, alpha), (center, center), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = BULLET_SPEED
        
    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

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