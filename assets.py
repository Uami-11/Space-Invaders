# assets.py (updated to upscale sprites)
import pygame
import os

def load_image(name, scale_factor=2.0):
    path = os.path.join("assets", "images", name)
    image = pygame.image.load(path).convert()  # Using .convert() as per previous fix
    # Scale the image
    new_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
    return pygame.transform.scale(image, new_size)

def load_animation(base_name, num_frames, scale_factor=2.0):
    frames = []
    for i in range(1, num_frames + 1):
        filename = f"{base_name}{i}.png"
        img = load_image(filename, scale_factor)
        frames.append(img)
    return frames

# Single images (scaled 2x)
PLAYER_IMG = load_image("player.png")
PLAYER_EXPLOSION_IMG = load_image("player_explosion.png")
MYSTERY_IMG = load_image("mystery_ship.png")
ENEMY_EXPLOSION_IMG = load_image("enemy_explosion.png")
BARRIER_IMG = load_image("barrier.png")

# Animated enemies (2 frames each, scaled)
ENEMY_FRAMES = {
    "front": load_animation("enemy_front", 2),
    "middle": load_animation("enemy_middle", 2),
    "back": load_animation("enemy_back", 2)
}

# Animated bullets (4 frames for player, 6 for enemy, scaled)
PLAYER_BULLET_FRAMES = load_animation("player_bullet", 4)
ENEMY_BULLET_FRAMES = load_animation("enemy_bullet", 5)

# Sounds (unchanged)
SHOOT_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "player_shoot.wav"))
PLAYER_DEATH_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "player_death.wav"))
ENEMY_SHOOT_SOUNDS = [
    pygame.mixer.Sound(os.path.join("assets", "sounds", "enemy_shoot1.wav")),
    pygame.mixer.Sound(os.path.join("assets", "sounds", "enemy_shoot2.wav"))
]
MYSTERY_SOUND = pygame.mixer.Sound(os.path.join("assets", "sounds", "mystery_ship.wav"))