import os

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
WAVE_TRANSITION_TIME = 1000
WAVE_SPEEDUP = 100
WAVE_ENEMY_MULTIPLIER = 1.5  # Coefficient multiplicateur d'ennemis par vague
SHOOTER_ENEMY_CHANCE = 0.3  # 30% de chance d'avoir un ennemi qui tire
ENEMY_BULLET_DAMAGE = 15

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Dossier src
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
EFFECTS_DIR = os.path.join(ASSETS_DIR, "effects")

# Assets paths
PLAYER_SPRITE = os.path.join(ASSETS_DIR, "player.png")
ENEMY_SPRITE = os.path.join(ASSETS_DIR, "enemy.png")
SHOOTER_ENEMY_SPRITE = os.path.join(ASSETS_DIR, "shooter_enemy.png")
BULLET_SPRITE = os.path.join(ASSETS_DIR, "bullet.png")
ENEMY_BULLET_SPRITE = os.path.join(ASSETS_DIR, "enemy_bullet.png")
GAME_LOGO = os.path.join(ASSETS_DIR, "logo.png")

# Sound paths
SOUND_DIR = os.path.join(ASSETS_DIR, "sounds")
SHOOT_SOUND = os.path.join(SOUND_DIR, "shoot.wav")
ENEMY_SHOOT_SOUND = os.path.join(SOUND_DIR, "enemy_shoot.wav")
HIT_SOUND = os.path.join(SOUND_DIR, "hit.wav")
ENEMY_DEATH_SOUND = os.path.join(SOUND_DIR, "enemy_death.wav")
PLAYER_HURT_SOUND = os.path.join(SOUND_DIR, "player_hurt.wav")
GAME_MUSIC = os.path.join(SOUND_DIR, "game_music.mp3")

# Fireball settings
FIREBALL_SPRITE = os.path.join(EFFECTS_DIR, "Part 3 Free.gif")
FIREBALL_FRAME_SIZE = 32  # Taille originale dans le spritesheet
FIREBALL_SCALE = 2.5     # Facteur d'échelle pour les boules de feu
FIREBALL_SIZE = int(FIREBALL_FRAME_SIZE * FIREBALL_SCALE)  # Taille finale

# Fireball colors (positions dans le spritesheet)
FIREBALL_COLORS = {
    "RED": 0,      # Première ligne
    "ORANGE": 1,   # Deuxième ligne
    "PURPLE": 2,   # Troisième ligne
    "BLUE": 3,     # Quatrième ligne
    "GREEN": 4,    # Cinquième ligne
    "RAINBOW": 5   # Sixième ligne
}

# Vérification de l'existence du fichier
if not os.path.exists(FIREBALL_SPRITE):
    print(f"ATTENTION: Le fichier {FIREBALL_SPRITE} n'existe pas!")
    print(f"Chemin complet attendu: {os.path.abspath(FIREBALL_SPRITE)}")

# Bullet effects settings
BULLET_COLORS = {
    "PLAYER": {
        "CORE": (160, 50, 255),     # Violet clair
        "GLOW": (200, 100, 255),    # Violet plus clair
        "TRAIL": (180, 70, 255, 80) # Violet avec transparence
    },
    "ENEMY": {
        "CORE": (255, 60, 60),      # Rouge vif
        "GLOW": (255, 100, 100),    # Rouge clair
        "TRAIL": (255, 80, 80, 80)  # Rouge avec transparence
    }
}

# Optimisation des effets
MAX_TRAIL_LENGTH = 5  # Limite la longueur de la traînée
TRAIL_UPDATE_FREQUENCY = 2  # Met à jour la traînée tous les N frames
BULLET_SURFACE_SIZE = 32  # Taille fixe pour les surfaces de projectiles

# Ajoutez ces constantes
SOUND_ON_COLOR = (0, 255, 0)  # Vert pour le son activé
SOUND_OFF_COLOR = (255, 0, 0)  # Rouge pour le son désactivé
SOUND_BUTTON_SIZE = 30
SOUND_BUTTON_PADDING = 10

# 3D Settings
PERSPECTIVE_SCALE = 1.5  # Facteur d'échelle pour l'effet de perspective
Z_DISTANCE = 500  # Distance de base pour l'effet 3D
ROTATION_SPEED = 2  # Vitesse de rotation des vaisseaux
TILT_ANGLE = 15  # Angle maximum d'inclinaison des vaisseaux

# Spaceship colors
SHIP_GLOW = (100, 100, 255, 128)  # Lueur des vaisseaux
ENGINE_COLORS = [(50, 100, 255), (100, 150, 255), (150, 200, 255)]  # Couleurs des réacteurs

# Score settings
SCORE_FILE = os.path.join(BASE_DIR, "data", "highscore.json")

