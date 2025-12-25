# assets.py
import pygame
import os

def load_image(name):
    path = os.path.join("assets", "images", name)
    return pygame.image.load(path).convert_alpha()

def load_animation(base_name, num_frames):
    frames = []
    for i in range(1, num_frames + 1):
        filename = f"{base_name}{i}.png"
        img = load_image(filename)
        frames.append(img)
    return frames

# Single images
PLAYER_IMG = load_image("player.png")
PLAYER_EXPLOSION_IMG = load_image("player_explosion.png")
MYSTERY_IMG = load_image("mystery_ship.png")
ENEMY_EXPLOSION_IMG = load_image("enemy_explosion.png")
BARRIER_IMG = load_image("barrier.png")

# Animated enemies (2 frames each)
ENEMY_FRAMES = {
    "front": load_animation("enemy_front", 2),
    "middle": load_animation("enemy_middle", 2),
    "back": load_animation("enemy_back", 2)
}

# Animated bullets (4 frames for player, 6 for enemy)
PLAYER_BULLET_FRAMES = load_animation("player_bullet", 4)
ENEMY_BULLET_FRAMES = load_animation("enemy_bullet", 5)

# Sounds
SHOOT_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "player_shoot.wav"))
PLAYER_DEATH_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "player_death.wav"))
ENEMY_SHOOT_SOUNDS = [
    pygame.mixer.Sound(os.path.join("assets", "sounds", "enemy_shoot1.wav")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "enemy_shoot2.wav"))
]
MYSTERY_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "mystery_ship.wav"))