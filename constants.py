# constants.py (unchanged - included for completeness)
import pygame

# Initialize pygame early to ensure font subsystem is ready
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts - using custom pixel font
PIXEL_FONT_PATH = "assets/fonts/determination-mono.ttf"
FONT = pygame.font.Font(PIXEL_FONT_PATH, 48)          # Title
SMALL_FONT = pygame.font.Font(PIXEL_FONT_PATH, 32)     # UI / instructions

# Game states
START_SCREEN = 0
PLAYING = 1
GAME_OVER = 2