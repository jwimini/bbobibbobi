import pygame
import random
from datetime import datetime
from datetime import timedelta
import time


def writeScore(count):
    global screen
    font = pygame.font.Font(None, 40)
    text = font.render('Point : ' + str(count), True, (160, 82, 45))
    screen.blit(text, (20, 20))


def writeMessage(text, count):
    global screen
    textfont = pygame.font.Font(None, 60)
    text = textfont.render(text, True, (255, 0, 0))
    count = textfont.render(f'{count}', True, (255, 0, 0))
    textpos = text.get_rect()
    countpos = count.get_rect()
    textpos.center = (480 / 2, 640 / 2 - 100)
    countpos.center = (480 / 2, 640 / 2)
    screen.blit(text, textpos)
    screen.blit(count, countpos)
    pygame.display.update()


def initGame():
    global WHITE, RED, GREEN, BLUE, DEEPBLUE, size, screen, done, clock, last_moved_time, KEY_DIRECTION
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (126, 218, 89)
    BLUE = (15, 124, 247)
    DEEPBLUE = (0, 0, 205)
    size = [500, 700]  # 화면 크기
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("스네이크 게임")
    done = False
    clock = pygame.time.Clock()
    last_moved_time = datetime.now()

    KEY_DIRECTION = {
        pygame.K_UP: 'N',
        pygame.K_DOWN: 'S',
        pygame.K_LEFT: 'W',
        pygame.K_RIGHT: 'E',
    }


def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 20, position[0] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(0, 2), (0, 1), (0, 0)]  # 뱀의 위치
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, BLUE, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'N':
            self.positions.append((y - 1, x))
        elif self.direction == 'S':
            self.positions.append((y + 1, x))
        elif self.direction == 'W':
            self.positions.append((y, x - 1))
        elif self.direction == 'C':
            self.positions.append((y, x + 1))


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)


# 4. pygame 무한루프
def runGame():
    global BLACK, RED, GREEN, BLUE, DEEPBLUE, size, screen, done, clock, last_moved_time, KEY_DIRECTION
    pygame.init()
    # 게임 시작 시, 뱀과 사과를 초기화
    snake = Snake()
    apple = Apple()

    count = 0

    while not done:
        clock.tick(10)
        screen.fill(GREEN)  # 배경 색

        snake.draw()
        apple.draw()
        # score_str = str(count).zfill(6)
        # score_image = large_font.render(score_str,True, (0, 255, 0))
        # screen.blit(score_image, (350, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        writeScore(count)

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        if snake.positions[0] == apple.position:
            snake.grow()
            count += 1
            apple.position = (random.randint(0, 19), random.randint(0, 19))

        if snake.positions[0] in snake.positions[1:]:
            done = True
            writeMessage('GAME OVER', count)
            time.sleep(3)

        pygame.display.update()

    pygame.quit()
