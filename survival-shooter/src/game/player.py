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
        
        # Chargement et configuration du sprite du joueur
        try:
            self.original_image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
            # Augmentation de la taille à 96x96 (PLAYER_SIZE * 3)
            self.original_image = pygame.transform.scale(self.original_image, (PLAYER_SIZE * 3, PLAYER_SIZE * 3))
            # Rotation initiale de 270 degrés (90 + 180)
            self.original_image = pygame.transform.rotate(self.original_image, 270)
            # Retournement horizontal du sprite
            self.original_image = pygame.transform.flip(self.original_image, True, False)
            self.image = self.original_image
        except Exception as e:
            print(f"Erreur lors du chargement de l'image du joueur: {e}")
            # Fallback au dessin par défaut avec la nouvelle taille
            self.original_image = pygame.Surface((PLAYER_SIZE * 3, PLAYER_SIZE * 3), pygame.SRCALPHA)
            center = PLAYER_SIZE * 1.5
            pygame.draw.circle(self.original_image, (*PLAYER_COLOR, 128), (center, center), PLAYER_SIZE * 1.5)
            pygame.draw.circle(self.original_image, PLAYER_COLOR, (center, center), PLAYER_SIZE)
            self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.trail = []
        self.angle = 0

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

        # Rotation en fonction de la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx))
        
        # Rotation du sprite
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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
                if hasattr(self, 'game') and self.game.shoot_sound and not self.game.sound_muted:
                    pygame.mixer.find_channel(True).play(self.game.shoot_sound)
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