import os
import sys
from math import sqrt
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_DOWN, K_SPACE
import time

# from tkinter import messagebox as msg, Tk


BLOCK_DATA = (
    (
        (0, 0, 1, \
         1, 1, 1, \
         0, 0, 0),
        (0, 1, 0, \
         0, 1, 0, \
         0, 1, 1),
        (0, 0, 0, \
         1, 1, 1, \
         1, 0, 0),
        (1, 1, 0, \
         0, 1, 0, \
         0, 1, 0),
    ), (
        (2, 0, 0, \
         2, 2, 2, \
         0, 0, 0),
        (0, 2, 2, \
         0, 2, 0, \
         0, 2, 0),
        (0, 0, 0, \
         2, 2, 2, \
         0, 0, 2),
        (0, 2, 0, \
         0, 2, 0, \
         2, 2, 0)
    ), (
        (0, 3, 0, \
         3, 3, 3, \
         0, 0, 0),
        (0, 3, 0, \
         0, 3, 3, \
         0, 3, 0),
        (0, 0, 0, \
         3, 3, 3, \
         0, 3, 0),
        (0, 3, 0, \
         3, 3, 0, \
         0, 3, 0)
    ), (
        (4, 4, 0, \
         0, 4, 4, \
         0, 0, 0),
        (0, 0, 4, \
         0, 4, 4, \
         0, 4, 0),
        (0, 0, 0, \
         4, 4, 0, \
         0, 4, 4),
        (0, 4, 0, \
         4, 4, 0, \
         4, 0, 0)
    ), (
        (0, 5, 5, \
         5, 5, 0, \
         0, 0, 0),
        (0, 5, 0, \
         0, 5, 5, \
         0, 0, 5),
        (0, 0, 0, \
         0, 5, 5, \
         5, 5, 0),
        (5, 0, 0, \
         5, 5, 0, \
         0, 5, 0)
    ), (
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6),
        (6, 6, 6, 6)
    ), (
        (0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0, \
         0, 7, 0, 0),
        (0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0, \
         0, 0, 0, 0),
        (0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0, \
         0, 0, 7, 0),
        (0, 0, 0, 0, \
         0, 0, 0, 0, \
         7, 7, 7, 7, \
         0, 0, 0, 0)
    )
)


class Block:
    """ 블록 객체 """

    def __init__(self, count):
        self.turn = randint(0, 3)
        self.type = BLOCK_DATA[randint(0, 6)]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = randint(2, 8 - self.size)
        self.ypos = 1 - self.size
        self.fire = count + INTERVAL

    def update(self, count):
        """ 블록 상태 갱신 (소거한 단의 수를 반환한다) """
        # 아래로 총돌?
        erased = 0
        if is_overlapped(self.xpos, self.ypos + 1, self.turn):
            for y_offset in range(BLOCK.size):
                for x_offset in range(BLOCK.size):
                    if 0 <= self.xpos + x_offset < WIDTH and \
                            0 <= self.ypos + y_offset < HEIGHT:
                        val = BLOCK.data[y_offset * BLOCK.size \
                                         + x_offset]
                        if val != 0:
                            FIELD[self.ypos + y_offset] \
                                [self.xpos + x_offset] = val

            erased = erase_line()
            go_next_block(count)

        if self.fire < count:
            self.fire = count + INTERVAL
            self.ypos += 1
        return erased

    def draw(self):
        """ 블록을 그린다 """

        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if 0 <= ypos + self.ypos < HEIGHT and \
                    0 <= xpos + self.xpos < WIDTH and val != 0:
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (x_pos, y_pos, 24, 24))


def writeScore(count):
    global SURFACE
    font = pygame.font.Font(None, 40)
    text = font.render(count, True, (153, 204, 153))
    SURFACE.blit(text, (360, 30))


# 게임 메시지 출력
def writeMessage(text, count):
    global SURFACE
    textfont = pygame.font.Font(None, 60)
    text = textfont.render(text, True, (255, 21, 0))
    count = textfont.render(f'{count}', True, (255, 21, 0))
    textpos = text.get_rect()
    countpos = count.get_rect()
    textpos.center = (480 / 2, 640 / 2 - 100)
    countpos.center = (480 / 2, 640 / 2)
    SURFACE.blit(text, textpos)
    SURFACE.blit(count, countpos)
    pygame.display.update()


def erase_line():
    """ 행이 모두 찬 단을 지운다 """
    erased = 0
    ypos = 20
    while ypos >= 0:
        if all(FIELD[ypos]):
            erased += 1
            del FIELD[ypos]
            FIELD.insert(0, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8])
        else:
            ypos -= 1
    return erased


def is_game_over():
    """ 게임 오버인지 아닌지 """
    filled = 0
    for cell in FIELD[0]:
        if cell != 0:
            filled += 1
    return filled > 2  # 2 = 좌우의 벽


def go_next_block(count):
    """ 다음 블록으로 전환한다 """
    global BLOCK, NEXT_BLOCK
    BLOCK = NEXT_BLOCK if NEXT_BLOCK != None else Block(count)
    NEXT_BLOCK = Block(count)


def is_overlapped(xpos, ypos, turn):
    # 블록이 벽이나 땅의 블록과 충돌하는지 아닌지
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if 0 <= xpos + x_offset < WIDTH and 0 <= ypos + y_offset < HEIGHT:
                if data[y_offset * BLOCK.size + x_offset] != 0 and FIELD[ypos + y_offset][xpos + x_offset] != 0:
                    return True
    return False


def main():
    """ 메인 루틴 """
    global SURFACE, SURFACE, FPSCLOCK, WIDTH, HEIGHT, INTERVAL, FIELD, COLORS, BLOCK, NEXT_BLOCK
    pygame.init()
    pygame.key.set_repeat(30, 30)
    SURFACE = pygame.display.set_mode([500, 660])
    pygame.display.set_caption("테트리스")
    FPSCLOCK = pygame.time.Clock()
    WIDTH = 12
    HEIGHT = 22
    INTERVAL = 40
    FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    COLORS = (
    (0, 0, 0), (255, 165, 0), (0, 0, 255), (0, 255, 255), (0, 255, 0), (255, 0, 255), (255, 255, 0), (255, 21, 0),
    (255, 153, 153))
    BLOCK = None
    NEXT_BLOCK = None
    count = 0
    score = 0
    game_over = False

    go_next_block(INTERVAL)

    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            FIELD[ypos][xpos] = 8 if xpos == 0 or xpos == WIDTH - 1 else 0
    for index in range(WIDTH):
        FIELD[HEIGHT - 1][index] = 8

    while not game_over:
        key = None
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                key = event.key

        game_over = is_game_over()
        if not game_over:
            count += 5
            if count % 1000 == 0:
                INTERVAL = max(1, INTERVAL - 2)
            erased = BLOCK.update(count)

            if erased > 0:
                score += (2 ** erased) * 100

            # 키 이벤트 처리
            next_x, next_y, next_t = \
                BLOCK.xpos, BLOCK.ypos, BLOCK.turn
            if key == K_SPACE:
                next_t = (next_t + 1) % 4
            elif key == K_RIGHT:
                next_x += 1
            elif key == K_LEFT:
                next_x -= 1
            elif key == K_DOWN:
                next_y += 1

            if not is_overlapped(next_x, next_y, next_t):
                BLOCK.xpos = next_x
                BLOCK.ypos = next_y
                BLOCK.turn = next_t
                BLOCK.data = BLOCK.type[BLOCK.turn]

        # 전체&낙하 중인 블록 그리기
        SURFACE.fill((0, 0, 51))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                val = FIELD[ypos][xpos]
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos * 25 + 25, ypos * 25 + 25, 24, 24))
        BLOCK.draw()

        # 다음 블록 그리기
        for ypos in range(NEXT_BLOCK.size):
            for xpos in range(NEXT_BLOCK.size):
                val = NEXT_BLOCK.data[xpos + ypos * NEXT_BLOCK.size]
                pygame.draw.rect(SURFACE, COLORS[val],
                                 (xpos * 25 + 350, ypos * 25 + 100, 24, 24))

        # 점수 나타내기
        score_str = str(score).zfill(6)
        writeScore(score_str)

        if game_over:
            writeMessage('GAME OVER', score)
            time.sleep(3)

        pygame.display.update()

        FPSCLOCK.tick(15)

    pygame.quit()
