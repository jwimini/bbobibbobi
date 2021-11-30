# import tkinter
# import tkinter as tk
#
#
# class Category:
#     def __init__(self):
#         self.category_run()
#
#
#     def category_run(self):
#         root = tk.Tk()
#         root.title("게임 고르기")
#         wall = tkinter.PhotoImage(file="img_/img/4.gif")  # 배경 이미지
#         wall_label = tkinter.Label(image=wall)
#         wall_label.place(x=0, y=0)
#         root.resizable(True, False)
#
#         # 창 크기 조절하기
#         w = 900  # 창 가로
#         h = 900  # 창 세로
#         ws = root.winfo_screenwidth()  # 모니터 가로
#         hs = root.winfo_screenheight()  # 모니터 세로
#         # 모니터 가운데에 위치
#         x = (ws / 2) - (w / 2) - 8  # x좌표 지정
#         y = (hs / 2) - (h / 2) - 31  # y좌표 지정
#         root.geometry('%dx%d+%d+%d' % (w, h, x, y))  # 창 크기, 위치 지정
#
#
#         # 게임 이동 버튼 만들기
#         btn1 = tk.Button(root, text='테트리스')
#         btn1.place(x=250, y=320, width=120, height=40)
#         btn2 = tk.Button(root, text='운석 피하기')
#         btn2.place(x=550, y=320, width=120, height=40)
#         btn3 = tk.Button(root, text='2048')
#         btn3.place(x=250, y=470, width=120, height=40)
#         btn4 = tk.Button(root, text='스네이크')
#         btn4.place(x=550, y=470, width=120, height=40)
#
#         # # 시작 버튼
#         # btn = tkinter.Button(root, text="start!" )  # 버튼 생성
#         # btn.place(x=300, y=550, width=350, height=60)  # 버튼 위치, 크기
#
#         root.mainloop()
#
#
# if __name__ == '__main__':
#     app = Category()
