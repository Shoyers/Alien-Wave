import pygame
import math
from utils.constants import *
from game.weapon import Bullet

class Player:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.health = 100
        self.score = 0
        # Surface principale du joueur
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        
        # Dessin du joueur avec un effet de "glow"
        center = PLAYER_SIZE // 2
        pygame.draw.circle(self.image, (*PLAYER_COLOR, 128), (center, center), PLAYER_SIZE//2)  # Aura
        pygame.draw.circle(self.image, PLAYER_COLOR, (center, center), PLAYER_SIZE//3)  # Corps
        
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.trail = []  # Pour l'effet de traînée

    def update(self):
        # Gestion du mouvement avec les touches ZQSD/WASD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] or keys[pygame.K_w]:  # Haut
            self.move(0, -PLAYER_SPEED)
        if keys[pygame.K_s]:  # Bas
            self.move(0, PLAYER_SPEED)
        if keys[pygame.K_q] or keys[pygame.K_a]:  # Gauche
            self.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_d]:  # Droite
            self.move(PLAYER_SPEED, 0)

        # Gestion du tir avec le clic gauche
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Clic gauche
            self.shoot()

        # Mise à jour des balles
        self.bullets.update()
        
        # Supprime les balles qui sortent de l'écran
        for bullet in self.bullets:
            if (bullet.rect.x < 0 or bullet.rect.x > SCREEN_WIDTH or 
                bullet.rect.y < 0 or bullet.rect.y > SCREEN_HEIGHT):
                bullet.kill()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Empêche le joueur de sortir de l'écran
        self.x = max(0, min(self.x, SCREEN_WIDTH))
        self.y = max(0, min(self.y, SCREEN_HEIGHT))
        self.rect.center = (self.x, self.y)

    def play_sound(self, sound_type):
        if hasattr(self, 'game'):
            print(f"Game instance exists, sound_muted: {self.game.sound_muted}")
            if not self.game.sound_muted:
                if sound_type == 'shoot' and self.game.shoot_sound:
                    print("Playing shoot sound")
                    self.game.shoot_sound.play()
                elif sound_type == 'hurt' and self.game.player_hurt_sound:
                    print("Playing hurt sound")
                    self.game.player_hurt_sound.play()
        else:
            print("No game instance found")

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= SHOOT_COOLDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.x
            dy = mouse_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance != 0:
                direction = (dx/distance, dy/distance)
                bullet = Bullet(self.x, self.y, direction)
                self.bullets.add(bullet)
                self.play_sound('shoot')
                self.last_shot = current_time

    def draw(self, screen):
        # Dessin des projectiles
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # Dessin du joueur
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.health -= amount
        self.play_sound('hurt')
        if self.health <= 0:
            self.die()

    def die(self):
        # Logic for player death
        pass

    def gain_score(self, points):
        self.score += points