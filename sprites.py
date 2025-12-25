# sprites.py (minor tweaks for scaling consistency)
import pygame
import random

from assets import *
from constants import WIDTH, HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 50  # Moved up slightly for better look
        self.speed = 8
        self.lives = 3
        self.hidden = False
        self.hide_timer = 0

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH // 2

        keys = pygame.key.get_pressed()
        if not self.hidden:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed

            self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def shoot(self):
        if not self.hidden:
            return Bullet(
                self.rect.centerx,
                self.rect.top,
                PLAYER_BULLET_FRAMES,
                -12,  # Faster bullet
            )
        return None

    def die(self):
        self.lives -= 1
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        PLAYER_DEATH_SOUND.play()
        explosion = Explosion(self.rect.center, PLAYER_EXPLOSION_IMG)
        return explosion, self.lives <= 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type_):
        super().__init__()
        self.type = type_
        self.frames = ENEMY_FRAMES[type_]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score_value = {"front": 10, "middle": 20, "back": 30}[type_]
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 500  # ms per frame for enemy animation

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = now

    def shoot(self):
        random.choice(ENEMY_SHOOT_SOUNDS).play()
        return Bullet(
            self.rect.centerx,
            self.rect.bottom,
            ENEMY_BULLET_FRAMES,
            8,  # Faster bullet
        )


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = MYSTERY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width
        self.rect.y = 80  # Slightly lower to avoid UI overlap
        self.speed = 5  # Faster for scaled size
        MYSTERY_SOUND.play()

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, speed):
        super().__init__()
        self.frames = frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60  # ms per frame for bullet animation

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = now

        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BARRIER_IMG.copy()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hits = 0
        self.max_hits = 5

    def take_hit(self):
        self.hits += 1
        alpha = int(255 * (1 - self.hits / self.max_hits))
        self.image = self.original_image.copy()
        self.image.set_alpha(alpha)
        if self.hits >= self.max_hits:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.kill()
