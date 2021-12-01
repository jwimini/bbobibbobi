import pygame
import sys
import random
import math
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_SPACE, Rect


class Block:
    def __init__(self, col, rect, speed=0):
        self.col = col
        self.rect = rect
        self.speed = speed
        self.dir = random.randint(-45, 45) + 270

    def move(self):  # 공을 움직인다 , radians를 사용해서 dir을 라디안으로 변환, X축과Y축의 방향성분구분
        self.rect.centerx += math.cos(math.radians(self.dir)) * self.speed
        self.rect.centery -= math.sin(math.radians(self.dir)) * self.speed

    def draw_E(self):
        pygame.draw.ellipse(SURFACE, self.col, self.rect)

    def draw_R(self):
        pygame.draw.rect(SURFACE, self.col, self.rect)


pygame.init()
pygame.display.set_caption('Block_Breaker!!')
pygame.key.set_repeat(10, 10)
SURFACE = pygame.display.set_mode((800, 800))
FPSCLOCK = pygame.time.Clock()


def main():
    Game_Start = False
    Score = 0
    BLOCK = []
    PADDLE = Block((200, 200, 0), Rect(375, 700, 100, 30))
    BALL = Block((200, 200, 0), Rect(375, 650, 20, 20), 10)
    colors = [(255, 0, 0), (255, 150, 0), (255, 228, 0), (11, 201, 4), (0, 84, 255), (0, 0, 147), (201, 0, 167)]
    for y, color in enumerate(colors, start=0):
        for x in range(0, 9):
            BLOCK.append(Block(color, Rect(x * 80 + 150, y * 40 + 40, 60, 20)))

    Bigfont = pygame.font.SysFont(None, 80)
    Smallfont = pygame.font.SysFont(None, 50)
    M_Game_Start1 = Bigfont.render("DO YOU WANT GAME START?", True, (255, 255, 255))
    M_Game_Start2 = Bigfont.render("CLICK THE SPACE BAR", True, (255, 255, 255))
    M_CLEAR = Bigfont.render("CLEAR!!", True, (255, 255, 255))
    M_FAIL = Bigfont.render("FAILED", True, (255, 0, 0))

    while True:
        M_SCORE = Smallfont.render("SCORE : {}".format(Score), True, (255, 255, 255))
        M_SPEED = Smallfont.render("SPEED : {}".format(BALL.speed), True, (255, 255, 255))
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    PADDLE.rect.centerx -= 10
                elif event.key == K_RIGHT:
                    PADDLE.rect.centerx += 10
                elif event.key == K_SPACE:
                    Game_Start = True

        if Game_Start == False:
            SURFACE.blit(M_Game_Start1, (80, 280))
            SURFACE.blit(M_Game_Start2, (180, 380))

        else:
            SURFACE.blit(M_SCORE, (250, 500))
            SURFACE.blit(M_SPEED, (550, 500))

            LenBlock = len(BLOCK)
            BLOCK = [x for x in BLOCK if not x.rect.colliderect(BALL.rect)]
            if len(BLOCK) != LenBlock:
                Score += 10
                BALL.dir *= -1

            if BALL.rect.centery < 1000:
                BALL.move()

            # 패들과 공이 부딪힘

            if PADDLE.rect.colliderect(BALL.rect):  # colliderect은 볼과 패들의 충돌 여부를 검사합니다.
                BALL.speed += 0.25
                BALL.dir = 90 + (PADDLE.rect.centerx - BALL.rect.centerx) / PADDLE.rect.width * 100

            # 패들이 게임틀안에 존재

            if PADDLE.rect.centerx < 55:
                PADDLE.rect.centerx = 55
            if PADDLE.rect.centerx > 945:
                PADDLE.rect.centerx = 945

            if BALL.rect.centerx < 0 or BALL.rect.centerx > 1000:
                BALL.dir = 180 - BALL.dir  # 반사각만큼 방향 변화

            elif BALL.rect.centery < 0:
                BALL.dir = -BALL.dir

            if len(BLOCK) == 0:
                SURFACE.blit(M_CLEAR, (380, 400))
            if BALL.rect.centery > 770 and len(BLOCK) > 0:
                SURFACE.blit(M_FAIL, (380, 400))
            BALL.draw_E()
            PADDLE.draw_R()
            for i in BLOCK:
                i.draw_R()

        pygame.display.update()
        FPSCLOCK.tick(30)

# if __name__ == '__main__':
#     main()
