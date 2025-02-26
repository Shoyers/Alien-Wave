# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)  # Ajout de la couleur blanche
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BG_COLOR = (15, 10, 20)  # Fond plus sombre
PLAYER_COLOR = (220, 130, 240)  # Violet néon pour le joueur
ENEMY_COLOR = (200, 30, 60)  # Rouge sang pour les ennemis
SHOOTER_ENEMY_COLOR = (255, 165, 0)  # Orange pour les ennemis qui tirent
BULLET_COLOR = (160, 50, 255)  # Violet clair pour les projectiles
HEALTH_COLOR = (220, 50, 50)  # Rouge vif pour la santé
XP_COLOR = (80, 220, 255)  # Bleu néon pour l'XP

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 32

# Weapon settings
BULLET_SPEED = 10
BULLET_SIZE = 5
BULLET_DAMAGE = 25
SHOOT_COOLDOWN = 250  # Délai entre chaque tir (en millisecondes)

# Enemy settings
ENEMY_SIZE = 30
ENEMY_DAMAGE = 10
ENEMY_SCORE = 100

# Game states
PLAYING = "playing"
GAME_OVER = "game_over"

# Colors for menu
OVERLAY_COLOR = (0, 0, 0, 128)  # Noir semi-transparent

# Particle effects
PARTICLE_COLORS = [(255, 50, 50), (255, 100, 100), (255, 150, 150)]
PARTICLE_SIZE = 4
PARTICLE_LIFETIME = 30

# Visual effects
GLOW_EFFECT = True
TRAIL_EFFECT = True

# Wave settings
ENEMIES_PER_WAVE = 10
WAVE_TRANSITION_TIME = 3000
WAVE_SPEEDUP = 100
SHOOTER_ENEMY_CHANCE = 0.3  # 30% de chance d'avoir un ennemi qui tire
ENEMY_BULLET_DAMAGE = 15

# Assets paths
ASSETS_DIR = "src/assets"
PLAYER_SPRITE = f"{ASSETS_DIR}/player.png"
ENEMY_SPRITE = f"{ASSETS_DIR}/enemy.png"
SHOOTER_ENEMY_SPRITE = f"{ASSETS_DIR}/shooter_enemy.png"
BULLET_SPRITE = f"{ASSETS_DIR}/bullet.png"