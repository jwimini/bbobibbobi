from pygame.locals import *
from random import randint
import time
import pygame

playing = True
moveUp = moveDown = moveRight = moveLeft = move_init = False

step = 23
score = 0
length = 2
speed = 75


x_snake_position = [0]
y_snake_position = [0]


for i in range(0, 1000):
    x_snake_position.append(-100)
    y_snake_position.append(-100)


def collision(x_coordinates_1, y_coordinates_1, x_coordinates_2, y_coordinates_2, size_snake, size_fruit):
    if ((x_coordinates_1 + size_snake >= x_coordinates_2) or (
            x_coordinates_1 >= x_coordinates_2)) and x_coordinates_1 <= x_coordinates_2 + size_fruit:
        if ((y_coordinates_1 >= y_coordinates_2) or (
                y_coordinates_1 + size_snake >= y_coordinates_2)) and y_coordinates_1 <= y_coordinates_2 + size_fruit:
            return True
        return False


def disp_score(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    window.blit(text, (400, 0))


pygame.init()

# gui 이름

window = pygame.display.set_mode((500, 500))
window_rect = window.get_rect()
pygame.display.set_caption("Snake game")

# 창 크기

cover = pygame.Surface(window.get_size())
cover = cover.convert()
cover.fill((250, 250, 250))
window.blit(cover, (0, 0))



pygame.display.flip()

# 기본 이미지 설정
head = pygame.image.load("img/img/head.png").convert_alpha()  # The head
head = pygame.transform.scale(head, (35, 35))

body_part_1 = pygame.image.load("img/img/body.png").convert_alpha()  # The body
body_part_1 = pygame.transform.scale(body_part_1, (25, 25))

fruit = pygame.image.load("img/img/strawberry.png").convert_alpha()  # The fruit
fruit = pygame.transform.scale(fruit, (35, 35))


position_1 = head.get_rect()
position_fruit = fruit.get_rect()



x_snake_position[0] = position_1.x
y_snake_position[0] = position_1.y

# 과일 위치

position_fruit.x = randint(2, 10) * step
position_fruit.y = randint(2, 10) * step
# Main loop for the game

while (playing == True):



    for event in pygame.event.get():


        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            playing = False



        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                if moveUp == False and move_init == True:  # Vérification que la direction soit différente et annonce que les déplacement on débutés
                    if moveDown == True:  # Empêchement d'aller dans la direction opposée
                        moveUp == False

                    else:

                        moveDown = moveRight = moveLeft = False  # Changement de la variable de déplacement
                        moveUp = move_init = True

            if event.key == pygame.K_DOWN:

                if moveDown == False:  # Empêchement d'aller dans la direction opposée
                    if moveUp == True:
                        moveDown == False
                    else:
                        moveRight = moveLeft = moveUp = False
                        moveDown = move_init = True

            if event.key == pygame.K_RIGHT:

                if moveRight == False:
                    if moveLeft == True:
                        moveRight == False
                    else:
                        moveLeft = moveUp = moveDown = False
                        moveRight = move_init = True
            if event.key == pygame.K_LEFT:
                if moveLeft == False:
                    if moveRight == True:
                        moveLeft == False
                    else:
                        moveRight = moveDown = moveUp = False
                        moveLeft = move_init = True

    window.blit(body_part_1, (-5, 5))
    window.blit(head, (0, 0))

    for i in range(length - 1, 0, -1):
        x_snake_position[i] = x_snake_position[(i - 1)]
        y_snake_position[i] = y_snake_position[(i - 1)]
    cover.fill((250, 250, 250))
    for i in range(1, length):
        cover.blit(body_part_1, (x_snake_position[i], y_snake_position[i]))

    if moveUp:
        y_snake_position[0] = y_snake_position[0] - step
        window.blit(cover, (0, 0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))
    if moveDown:
        y_snake_position[0] = y_snake_position[0] + step
        window.blit(cover, (0, 0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))
    if moveRight:
        x_snake_position[0] = x_snake_position[0] + step
        window.blit(cover, (0, 0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))
    if moveLeft:
        x_snake_position[0] = x_snake_position[0] - step
        window.blit(cover, (0, 0))
        window.blit(head, (x_snake_position[0], y_snake_position[0]))
    if x_snake_position[0] < window_rect.left:
        playing = False
    if x_snake_position[0] + 35 > window_rect.right:
        playing = False
    if y_snake_position[0] < window_rect.top:
        playing = False
    if y_snake_position[0] + 35 > window_rect.bottom:
        playing = False
    if collision(x_snake_position[0], y_snake_position[0], x_snake_position[i], y_snake_position[i], 0, 0) and (
            move_init == True):
        playing = False

    window.blit(fruit, position_fruit)

    if collision(x_snake_position[0], y_snake_position[0], position_fruit.x, position_fruit.y, 35, 25):

        position_fruit.x = randint(1, 20) * step
        position_fruit.y = randint(1, 20) * step

        for j in range(0, length):

            while collision(position_fruit.x, position_fruit.y, x_snake_position[j], y_snake_position[j], 35, 25):
                position_fruit.x = randint(1, 20) * step
                position_fruit.y = randint(1, 20) * step

        length = length + 1
        score = score + 1

    disp_score(score)

    pygame.display.flip()

    time.sleep(speed / 1000)

pygame.quit()
exit()