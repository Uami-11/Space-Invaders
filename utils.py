# utils.py
import pygame
from constants import *

def draw_text(screen, text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

def show_start_screen(screen):
    screen.fill(BLACK)
    draw_text(screen, "SPACE INVADERS", FONT, WHITE, WIDTH//2, HEIGHT//3)
    draw_text(screen, "Press any key to start", SMALL_FONT, WHITE, WIDTH//2, HEIGHT//2)
    pygame.display.flip()

def show_game_over(screen, score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", FONT, WHITE, WIDTH//2, HEIGHT//3)
    draw_text(screen, f"Score: {score}", SMALL_FONT, WHITE, WIDTH//2, HEIGHT//2 - 50)
    draw_text(screen, "Try Again (R)", SMALL_FONT, WHITE, WIDTH//2, HEIGHT//2 + 20)
    draw_text(screen, "Quit (Q)", SMALL_FONT, WHITE, WIDTH//2, HEIGHT//2 + 70)
    pygame.display.flip()