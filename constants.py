import pygame

# Initialize pygame early to ensure font subsystem is ready
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts - now using your custom pixel font for that retro look!
PIXEL_FONT_PATH = "fonts/determination-mono.ttf"  # Adjust if filename is different (e.g., .ttf vs .TTF)

FONT = pygame.font.Font(PIXEL_FONT_PATH, 48)          # Larger for title
SMALL_FONT = pygame.font.Font(PIXEL_FONT_PATH, 32)     # Smaller for UI / instructions

# Game states
START_SCREEN = 0
PLAYING = 1
GAME_OVER = 2