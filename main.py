import tkinter
import tkinter as tk

import pygame
pygame.init()

root = tk.Tk()
root.title("뽀글뽀글 미니게임")
wall = tkinter.PhotoImage(file="./img/1.gif")     # 배경 이미지
wall_label = tkinter.Label(image=wall)
wall_label.place(x=0, y=0)

# 배경음악 지정
music = pygame.mixer.Sound('PyRacing/sound/bg.ogg')
# 배경음악 무한 반복
music.play(-1)

# 창 크기 조절하기
w = 900   # 창 가로
h = 900     # 창 세로
ws = root.winfo_screenwidth()   # 모니터 가로
hs = root.winfo_screenheight()  # 모니터 세로
# 모니터 가운데에 위치
x = (ws/2) - (w/2) - 8      # x좌표 지정
y = (hs/2) - (h/2) - 31     # y좌표 지정
root.geometry('%dx%d+%d+%d' % (w, h, x, y))     # 창 크기, 위치 지정

btn = tkinter.Button(root, text="press start")     # 버튼 생성
btn.place(x=292, y=650, width=350, height=60)   # 버튼 위치, 크기

root.resizable(True, False)
root.mainloop()
