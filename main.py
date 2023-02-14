import pygame
import random
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 1200, 650

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('verdana', 20)

main_surface = pygame.display.set_mode(screen)
IMGS_PATH = 'Бандерогусак для анімації (goose)'
#ball = pygame.Surface((20, 20))
#ball.fill(WHITE)
ball_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = ball_imgs[0]
#ball = pygame.image.load('player.png').convert_alpha()
ball_rect = ball.get_rect()
ball_speed = 5
ball_fill = WHITE

def create_enemy():
    #enemy = pygame.Surface((20, 20))
    #enemy.fill(RED)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (200, 50))
    enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    #bonus = pygame.Surface((20, 20))
    #bonus.fill(GREEN)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

bonuses = []

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

enemies = []

is_working = True
scores = 0
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

img_index = 0

while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len (ball_imgs):
                img_index = 0
            ball = ball_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    #main_surface.fill((0, 0, 0))
    #main_surface.blit(bg, (0, 0))
    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(ball, ball_rect)

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 30, 0))
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= heigth:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            scores += 1
            bonuses.pop(bonuses.index(bonus))

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= heigth:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)

    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    #enemy_rect = enemy_rect.move(-enemy_speed, 0)

    #ball_rect = ball_rect.move(ball_speed)

    #if ball_rect.bottom >= heigth or ball_rect.top <= 0:
     #   ball_speed[1] = -ball_speed[1]

      #  if ball_fill == WHITE:
       #     ball.fill(RED)
        #    ball_fill = RED
        #else:
         #   ball.fill(WHITE)
          #  ball_fill = WHITE


    #if ball_rect.right >= width or ball_rect.left <= 0:
     #   ball_speed[0] = -ball_speed[0]

      #  if ball_fill == WHITE:
         #   ball.fill(RED)
        #    ball_fill = RED
       # else:
          #  ball.fill(WHITE)
           # ball_fill = WHITE
    pygame.display.flip()