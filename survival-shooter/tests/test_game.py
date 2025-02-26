import pytest
import pygame
from src.game.weapon import Weapon, Bullet

def test_bullet_creation():
    bullet = Bullet(100, 100, (1, 0))
    assert bullet.rect.center == (100, 100)
    assert bullet.direction == (1, 0)

def test_weapon_cooldown():
    weapon = Weapon()
    weapon.shoot((0, 0), (100, 0))
    assert len(weapon.bullets) == 1
    # Test cooldown    import pytest
    import pygame
    import sys
    import os
    
    # Ajoutez le chemin du dossier parent au PYTHONPATH
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.game.weapon import Weapon, Bullet
    
    weapon.shoot((0, 0), (100, 0))
    assert len(weapon.bullets) == 1  # Should not create new bullet during cooldown

def test_bullet_movement():
    bullet = Bullet(100, 100, (1, 0))
    initial_x = bullet.rect.x
    bullet.update()
    assert bullet.rect.x > initial_x