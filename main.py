# main.py (updated enemy movement and game-over logic)
import pygame
import random
import sys

from constants import *

# pygame.mixer.init() for sound
pygame.mixer.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
from sprites import *
from utils import *
from assets import *

CLOCK = pygame.time.Clock()

# Groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
barriers = pygame.sprite.Group()

game_state = START_SCREEN
score = 0
player = None


def start_game():
    global player, score, enemy_direction, enemy_speed, mystery_timer, last_enemy_shoot

    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    enemy_bullets.empty()
    barriers.empty()

    score = 0
    player = Player()
    all_sprites.add(player)

    # Create enemies (compact formation)
    for row in range(5):
        enemy_type = "back" if row == 0 else "middle" if row < 3 else "front"
        for col in range(11):
            enemy = Enemy(80 + col * 40, 60 + row * 40, enemy_type)
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Create barriers
    for i in range(4):
        x = 120 + i * 170
        barrier = Barrier(x, HEIGHT - 120)
        all_sprites.add(barrier)
        barriers.add(barrier)

    # Reset variables
    enemy_direction = 1
    enemy_speed = 1.5  # Initial speed
    mystery_timer = pygame.time.get_ticks() + random.randint(10000, 20000)
    last_enemy_shoot = 0

    return PLAYING


# Enemy movement variables
enemy_direction = 1
enemy_drop = 10  # Reduced from 20 for slower descent
enemy_speed = 1.5
max_enemy_speed = 3.0  # New: Cap speed to prevent "super fast" movement

# Mystery ship timer
mystery_timer = pygame.time.get_ticks() + random.randint(10000, 20000)

# Main loop
running = True
last_enemy_shoot = 0

while running:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == START_SCREEN:
                game_state = start_game()

            elif game_state == PLAYING:
                if event.key == pygame.K_SPACE:
                    bullet = player.shoot()
                    if bullet:
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        SHOOT_SOUND.play()

            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    game_state = start_game()
                elif event.key == pygame.K_q:
                    running = False
            elif game_state == WIN:
                if event.key == pygame.K_r:
                    game_state = start_game()
                elif event.key == pygame.K_q:
                    running = False

    if game_state == START_SCREEN:
        show_start_screen(SCREEN)
        continue

    elif game_state == GAME_OVER:
        show_game_over(SCREEN, score)
        continue
    elif game_state == WIN:
        show_win_screen(SCREEN, score)
        continue

    # === PLAYING STATE ===
    all_sprites.update()

    # Enemy formation movement
    move_down = False
    for enemy in enemies:
        enemy.rect.x += enemy_direction * enemy_speed

        if enemy.rect.right >= WIDTH - 20 or enemy.rect.left <= 20:
            move_down = True

        if enemy.rect.bottom >= HEIGHT - 50:  # Lowered from -100 for more play area
            game_state = GAME_OVER

    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.rect.y += enemy_drop
        enemy_speed = min(enemy_speed + 0.1, max_enemy_speed)

    # Random enemy shooting
    now = pygame.time.get_ticks()
    if now - last_enemy_shoot > random.randint(800, 2000) and enemies:
        shooter = random.choice(list(enemies))
        bullet = shooter.shoot()
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
        last_enemy_shoot = now

    # Mystery ship
    if now > mystery_timer:
        mystery = MysteryShip()
        all_sprites.add(mystery)
        mystery_timer = now + random.randint(10000, 20000)

    # Collisions
    # Player bullet hits enemy
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += hit.score_value
        explosion = Explosion(hit.rect.center, ENEMY_EXPLOSION_IMG)
        all_sprites.add(explosion)

    # Enemy bullet hits player
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in player_hits:
        explosion, game_over = player.die()
        all_sprites.add(explosion)
        if game_over:
            game_state = GAME_OVER

    # Bullets hit barriers
    for bullet_group in [bullets, enemy_bullets]:
        barrier_hits = pygame.sprite.groupcollide(barriers, bullet_group, False, True)
        for barrier in barrier_hits:
            barrier.take_hit()

    # Player bullet hits mystery ship
    mysteries = [s for s in all_sprites if isinstance(s, MysteryShip)]
    for mystery in mysteries:
        if pygame.sprite.spritecollide(mystery, bullets, True):
            score += 100
            explosion = Explosion(mystery.rect.center, ENEMY_EXPLOSION_IMG)
            all_sprites.add(explosion)
            mystery.kill()

    # Win condition (restart wave)
    if not enemies:
        game_state = WIN

    # Draw
    SCREEN.fill(BLACK)
    all_sprites.draw(SCREEN)

    # UI
    draw_text(SCREEN, f"Score: {score}", SMALL_FONT, WHITE, 20, 10, center=False)
    draw_text(
        SCREEN,
        f"Lives: {player.lives}",
        SMALL_FONT,
        WHITE,
        WIDTH - 150,
        10,
        center=False,
    )

    pygame.display.flip()

pygame.quit()
sys.exit()
