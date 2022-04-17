import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('main-icon.png')
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('ship-64px.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
delta = 0.5

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 20
for a in range(num_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(0.3)
    enemyY_change.append(10)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
# Winner text
win_font = pygame.font.Font('freesansbold.ttf', 64)


def defeat_enemy(i):
    enemy_img.pop(i)
    enemyX.pop(i)
    enemyY.pop(i)
    enemyX_change.pop(i)
    enemyY_change.pop(i)


def show_score(x, y):
    txt_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(txt_score, (x, y))


def game_over_text():
    text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 250))


def win_text():
    text = win_font.render("SIIIIIIIIIIUUUU", True, (255, 255, 255))
    screen.blit(text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance <= 30:
        return True
    else:
        return False


# Game Loop
running = True

press_left = False
press_right = False

while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    # Set ship
    player(playerX, playerY)

    for event in pygame.event.get():

        # Exit event
        if event.type == pygame.QUIT:
            running = False
        # If keystroke is pressed, check whether its right or left
        if event.type == pygame.KEYDOWN:
            # Move left
            if event.key == pygame.K_LEFT:
                playerX_change = -delta
                press_left = True
            # Move right
            if event.key == pygame.K_RIGHT:
                playerX_change = delta
                press_right = True
            # Move down
            if event.key == pygame.K_DOWN:
                playerY_change = delta
            # Move UP
            if event.key == pygame.K_UP:
                playerY_change = -delta
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of spaceship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                press_left = False
                if not press_right:
                    playerX_change = 0

            if event.key == pygame.K_RIGHT:
                press_right = False
                if not press_left:
                    playerX_change = 0

            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    if len(enemyY) == 0:
        win_text()

    to_kill = []
    # Limit enemy's movement
    for i in range(len(enemyY)):
        # Game Over
        print(enemyY[i])
        if enemyY[i] > 200:
            for j in range(len(enemyY)):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explossion_sound = mixer.Sound('explosion.wav')
            explossion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            to_kill.append(i)

    # Drop enemies from array
    for i in to_kill:
        defeat_enemy(i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
