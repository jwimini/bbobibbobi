import sys
import tkinter
import pygame

import block
import game_2048
import snake
import tetris

pygame.init()

main = tkinter.Tk()
main.title("뽀글뽀글 미니게임")


def tetrisGame():
    tetris.main()


def breakgame():
    block.main()


def Game2048():
    game_2048.Game()


def snakeGame():
    snake.initGame()
    snake.runGame()


def move_category():
    bg = tkinter.PhotoImage(file="img_/img/4.gif")  # 배경 이미지
    wall_label = tkinter.Label(image=bg)
    wall_label.place(x=0, y=0)
    btn1 = tkinter.Button(main, text='테트리스', command=tetrisGame)
    btn1.place(x=250, y=320, width=120, height=40)
    btn2 = tkinter.Button(main, text='블럭 깨기', command=breakgame)
    btn2.place(x=550, y=320, width=120, height=40)
    btn3 = tkinter.Button(main, text='2048', command=Game2048)
    btn3.place(x=250, y=470, width=120, height=40)
    btn4 = tkinter.Button(main, text='스네이크', command=snakeGame)
    btn4.place(x=550, y=470, width=120, height=40)
    main.mainloop()


pygame.init()
wall = tkinter.PhotoImage(file="img_/img/1.gif")  # 배경 이미지
wall_label = tkinter.Label(image=wall)
wall_label.place(x=0, y=0)

# 배경음악 지정
music = pygame.mixer.Sound('img_/sound/bg.ogg')
# 배경음악 무한 반복
music.play(-1)
music.set_volume(0.2)

# 창 크기 조절하기
w = 900  # 가로
h = 900  # 세로

ws = main.winfo_screenwidth()  # 가로
hs = main.winfo_screenheight()  # 세로

# 모니터 가운데에 위치
x = (ws / 2) - (w / 2) - 8  # x좌표
y = (hs / 2) - (h / 2) - 31  # y좌표
main.geometry('%dx%d+%d+%d' % (w, h, x, y))  # 창 크기, 위치 지정

btn = tkinter.Button(main, text="press start", command=move_category)  # 버튼 생성
btn.place(x=292, y=650, width=350, height=60)  # 버튼 위치, 크기

main.resizable(True, False)
main.mainloop()
