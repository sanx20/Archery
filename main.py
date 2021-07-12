import pygame
import random
import math
from pygame import mixer

pygame.init()  # initializing pygame
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
text_x = 10
text_y = 570


def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (192, 192, 192))
    screen.blit(score, (x, y))


# music
mixer.music.load('rainforest.wav')
mixer.music.play(-1)
# Icon & background
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption(' } Archery by Sanx ~~>')
icon = pygame.image.load('bow-and-arrow.png')
pygame.display.set_icon(icon)
background = pygame.image.load('back.png')

# apple
apple_img = pygame.image.load('ghost.png')
apple_x = random.randint(380, 500)
apple_y = 0
apple_y_change = 0

# apple2
apple_img_2 = pygame.image.load('ghost.png')
apple_x_2 = random.randint(380, 500)
apple_y_2 = 568
apple_y_change_2 = 0


def apple(x, y):
    screen.blit(apple_img, (x, y))


def apple_2(x, y):
    screen.blit(apple_img, (x, y))


# witch
witch_img = pygame.image.load('witch.png')
witch_x = 0
witch_y = 60
witch_x_change = 0.7
laugh = mixer.Sound('laugh.wav')
laugh.play()


def witch(x, y):
    screen.blit(witch_img, (x, y))


# player
player_img = pygame.image.load('bow.png')
player_x = 5
player_y = random.randint(0, 545)
player_y_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# target
target_img = pygame.image.load('target.png')
target_x = 735
target_y = random.randint(64, 545)
target_y_change = 1


def target(x, y):
    screen.blit(target_img, (x, y))


# arrow
arrow_img = pygame.image.load('rsz_1arrow.png')
arrow_x = 0
arrow_y = player_y
arrow_x_change = 10
arrow_state = 'ready'


def arrow(x, y):
    global arrow_state
    arrow_state = 'fire'
    screen.blit(arrow_img, (x + 16, y))


# collisons
score = 0


def target_collision(arrow_x, arrow_y, target_x, target_y):
    distance = math.sqrt((math.pow(arrow_x - target_x, 2)) + (math.pow(arrow_y - target_y, 2)))
    if distance < 30:
        return True


def apple_collision(arrow_x, arrow_y, apple_x, apple_y):
    distance = math.sqrt((math.pow(arrow_x - apple_x, 2)) + (math.pow(arrow_y - apple_y, 2)))
    if distance < 40:
        return True


def apple_2_collision(arrow_x, arrow_y, apple_x_2, apple_y_2):
    distance = math.sqrt((math.pow(arrow_x - apple_x_2, 2)) + (math.pow(arrow_y - apple_y_2, 2)))
    if distance < 40:
        return True


# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
val = 0


def game_over_text():
    over = over_font.render('GAME OVER', True, (0, 0, 0))
    screen.blit(over, (200, 250))

    # Game loop


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_y_change = -2.5
            if event.key == pygame.K_DOWN:
                player_y_change = 2.5
            if event.key == pygame.K_SPACE:
                if arrow_state == 'ready':
                    arrow_sound = mixer.Sound('flyby.wav')
                    arrow_sound.play()
                    arrow_y = player_y
                    arrow(arrow_x, arrow_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0
    # arrow
    if arrow_x >= 820:
        arrow_x = player_x + 16
        arrow_state = 'ready'
    if arrow_state == 'fire':
        arrow(arrow_x, arrow_y)
        arrow_x += arrow_x_change
    # ghost
    if apple_y > 568:
        apple_y_change = -apple_y_change
        apple_x = random.randint(300, 380)
    else:
        apple_y_change += 0.03
    apple_y += apple_y_change
    apple(apple_x, apple_y)

    if apple_y_2 < -50:
        apple_y_change_2 = -apple_y_change_2
        apple_x_2 = random.randint(400, 500)
    else:
        apple_y_change_2 -= 0.03
    apple_y_2 += apple_y_change_2
    apple_2(apple_x_2, apple_y_2)

    # witch
    if witch_x > 840:
        witch_x = -64
        witch_y = random.randint(0, 60)
        laugh = mixer.Sound('laugh.wav')
        laugh.play()
    witch_x += witch_x_change
    witch(witch_x, witch_y)
    if player_y <= 0:
        player_y = 0
    elif player_y >= 545:
        player_y = 545

    # target
    if target_y <= 0:
        target_y_change = random.uniform(0.5, 3)
    elif target_y >= 545:
        target_y_change = random.uniform(-3, -0.5)
    target_y += target_y_change
    target(target_x, target_y)

    # player
    player_y += player_y_change
    player(player_x, player_y)
    # collision
    if target_collision(arrow_x, arrow_y, target_x, target_y):
        target_sound = mixer.Sound('hitting_board-[AudioTrimmer.com].wav')
        target_sound.play()
        score_value += 1
    if apple_collision(arrow_x, arrow_y, apple_x, apple_y):
        slime_sound = mixer.Sound('Slime.wav')
        slime_sound.play()
        arrow_state = 'garbage'
        target_x = 2000
        player_x = 2000
        arrow_x = -50
        val += 1
    if apple_collision(arrow_x, arrow_y, apple_x_2, apple_y_2):
        arrow_state = 'garbage'
        slime_sound = mixer.Sound('Slime.wav')
        slime_sound.play()
        target_x = 2000
        player_x = 2000
        arrow_x = -50
        val += 1
    if val > 0:
        game_over_text()
    show_score(text_x, text_y)
    pygame.display.update()
