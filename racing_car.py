import sys
import pygame
import random
from tkinter import messagebox as msg
from tkinter import Tk

# 게임 방법 소개
root = Tk()
root.withdraw()
msg.showinfo('게임 방법', '레이싱게임은 방향키로 하는 게임 입니다!')

# 게임 화면 크기
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800

# 색상
GRAY = (150, 150, 150)

# 소스 디렉토리

DIRCARS = "PyRacing\\cars\\"

DIRSOUND = "PyRacing\\sound\\"

# 기본 변수

STAGE = 1

CAR_COUNT = 5

# 자동차 오브젝트를 저장할 List

CARS = []


class Car:
    car_image = ['Car01.png', 'Car02.png', 'Car03.png', 'Car04.png', 'Car05.png', \
                 'Car06.png', 'Car07.png', 'Car08.png', 'Car09.png', 'Car10.png', \
                 'Car11.png', 'Car12.png', 'Car13.png', 'Car14.png', 'Car15.png', \
                 'Car16.png', 'Car17.png', 'Car18.png', 'Car19.png', 'Car20.png', \
                 'Car21.png', 'Car22.png', 'Car23.png', 'Car24.png', 'Car25.png', \
                 'Car26.png', 'Car27.png', 'Car28.png', 'Car29.png', 'Car30.png', \
                 'Car31.png', 'Car32.png', 'Car33.png', 'Car34.png', 'Car35.png', \
                 'Car36.png', 'Car37.png', 'Car38.png', 'Car39.png', 'Car40.png']

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = ""

    def load_car(self):
        # 상대방 자동차

        # 40개의 이미지중에서 랜덤으로 선택한다.
        self.image = pygame.image.load(DIRCARS + random.choice(self.car_image))
        self.rect = self.image.get_rect()

        # 이미지 크기 조절 - 이미지마다 크기가 다 다르므로 가로 세로 비율 유지하면서 변경
        if self.rect.width <= 55:
            carwidth = self.rect.width - 15
            carheight = round((self.rect.height * carwidth) / self.rect.width)
        else:
            carwidth = self.rect.width
            carheight = self.rect.height

        self.image = pygame.transform.scale(self.image, (carwidth, carheight))
        self.rect.width = carwidth
        self.rect.height = carheight

        # 생성 위치 - 스크린 크기 안에서 랜덤으로 x 좌표 생성. y 좌표는 스크린 밖 위에 생성
        self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50)

        # STAGE에 따른 속도 변화, STAGE가 높아짐에 따라 자동차의 속도도 빨라진다.

        # 다양한 속도차이를 위해 5 ~ speed 사이에세 랜덤으로 속도를 선택하게 한다.
        speed = STAGE + 5
        if speed > 15:
            speed = 15
        self.dy = random.randint(5, speed)

    # 자동차를 스크린에 그리기

    def draw_car(self):
        SCREEN.blit(self.image, [self.rect.x, self.rect.y])

    # x 좌표 이동 - 플레이어 자동차의 움직임 제어할 때 필요

    def move_x(self):
        self.rect.x += self.dx

    # y 좌표 이동 - 플레이어 자동차의 움직임 제어할 때 필요,

    def move_y(self):
        self.rect.y += self.dy

    # 화면 밖으로 못 나가게 방지

    def check_screen(self):
        if self.rect.right > WINDOW_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

    # 차량 충돌 감지
    # distance : 오른쪽, 왼쪽, 아래쪽, 위쪽 이미지의 간격 설정

    def check_collision(self, car, distance=0):
        if (self.rect.top + distance < car.rect.bottom) and (car.rect.top < self.rect.bottom - distance) and (
                self.rect.left + distance < car.rect.right) and (car.rect.left < self.rect.right - distance):
            return True
        else:
            return False


def main():
    global SCREEN, CAR_COUNT, WINDOW_WIDTH, WINDOW_HEIGHT

    # pygame 초기화 및 스크린 생성

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                     pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("레이싱 게임")
    # 투명 아이콘은 32 x 32 로 해야 적용 됨
    windowicon = pygame.image.load(DIRCARS + 'icon.png').convert_alpha()
    pygame.display.set_icon(windowicon)

    clock = pygame.time.Clock()

    # 설정한 수 만큼 자동차 오브젝트 생성하여 CARS 리스트에 넣기

    for i in range(CAR_COUNT):
        car = Car(0, 0, 0, 0)
        car.load_car()
        CARS.append(car)

    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

        # 배경색을 회색으로
        SCREEN.fill(GRAY)

        # 다른 자동차들 도로위에 움직이기
        for i in range(CAR_COUNT):
            CARS[i].draw_car()
            CARS[i].rect.y += CARS[i].dy

            # 화면 아래로 내려가면 자동차를 다시 로드한다.
            # 로드시 자동차의 이미지가 랜덤으로 바뀌므로 새로운 자동차가 생긴 듯한 효과가 있다.
            if CARS[i].rect.y > WINDOW_HEIGHT:
                CARS[i].load_car()

        # 상대 자동차들끼리 충돌 감지, 각 자동차들을 순서대로 서로 비교
        for i in range(CAR_COUNT):
            for j in range(i + 1, CAR_COUNT):
                # 충돌 후 서로 팅겨 나가게 함.
                if CARS[i].check_collision(CARS[j]):
                    # 왼쪽에 있는 차는 왼쪽으로 오른쪽 차는 오른쪽으로 튕김
                    if CARS[i].rect.x > CARS[j].rect.x:
                        CARS[i].rect.x += 4
                        CARS[j].rect.x -= 4
                    else:
                        CARS[i].rect.x -= 4
                        CARS[j].rect.x += 4

                    # 위쪽 차는 위로, 아래쪽차는 아래로 튕김
                    if CARS[i].rect.y > CARS[j].rect.y:
                        CARS[i].rect.y += CARS[i].dy
                        CARS[j].rect.y -= CARS[j].dy
                    else:
                        CARS[i].rect.y -= CARS[i].dy
                        CARS[j].rect.y += CARS[j].dy

        pygame.display.flip()

        # 초당 프레임 설정
        clock.tick(60)


if __name__ == '__main__':
    main()
