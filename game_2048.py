import tkinter
import tkinter as tk
import random
import os

# Design parameters, color in Hex
from tkinter import messagebox
from tkinter import *
import pygame

pygame.init()

GRID_COLOR = "#E0E6F8"
# music = pygame.mixer.Sound('img_/sound/2048.ogg')
# # 배경음악 무한 반복
# music.play(-1)

EMPTY_CELL_COLOR = "#c2b3a9"
SCORE_LABEL_FONT = ("Verdana", 18)
SCORE_FONT = ("Helvetica", 24, "bold")
CELL_COLORS = {
    2: '#F88877',
    4: '#F8A964',
    8: '#E3E862',
    16: '#BFF876',
    32: '#81F8CC',
    64: '#80C9FA',
    128: '#838FFD',
    256: '#AD84F3',
    512: '#ECA0F8',
    1024: '#FB8AD7',
    2048: '#F398B2', 4096: '#D2BEF8'}
CELL_NUMBER_COLORS = {2: "#695c57", 4: "#695c57", 8: "#ffffff"}
CELL_NUMBER_FONTS = ("Helvetica", 15, "bold")

class Game(tk.Frame):
    def __init__(self):
        # Set main window
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.main_grid = tk.Frame(
            self, bg=GRID_COLOR, bd=3, width=100, height=100
        )
        self.main_grid.grid(pady=(100, 0))
        self.top_value = 2048

        self.grid_size = 4

        self.sw = self.master.winfo_screenwidth()
        self.sh = self.master.winfo_screenheight()

        self.make_GUI()
        self.create_button()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
        self.mainloop()

    def make_GUI(self):
        self.cells = []
        # Creating the grid
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell_frame = tk.Frame(
                    self.main_grid, bg=EMPTY_CELL_COLOR, width=80,height=80)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {'frame': cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        w = self.grid_size*91
        h = (self.grid_size+1)*93
        x = (self.sw - w)/2
        y = (self.sh - h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        act_frame = tk.Frame(self)
        act_frame.place(relx=0.10, rely=0.05, anchor="center",)
        tk.Label(
            act_frame,
            text="2048",
            font=SCORE_LABEL_FONT,).grid(row=0)

        button1 = tk.Button(self, text='Scores', command=lambda: self.score())
        button1.place(relx=0.1, rely=0.17, anchor="center")

        self.score = 0
        self.bstScore = 0

        # if os.path.exists("score.txt"):
        #     with open("score.txt", "r", encoding='utf-8') as f:
        #         self.score = int(f.read())

        if os.path.exists("bestscore.txt"):
            with open("bestscore.txt", "r") as f:
                self.bstScore = int(f.read())
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(score_frame,text="Score",font=SCORE_LABEL_FONT,).grid(row=0)
        self.score_label = tk.Label(score_frame, text=self.score, font=SCORE_FONT)
        self.score_label.grid(row=1)
        record_frame = tk.Frame(self)
        record_frame.place(relx=0.8, y=45, anchor="center")
        tk.Label(
            record_frame,
            text="Record",
            font=SCORE_LABEL_FONT,
        ).grid(row=0)
        self.record_label = tk.Label(record_frame, text= self.bstScore, font=SCORE_FONT)
        self.record_label.grid(row=2)


    def get_score(self):
        self.score = []
        # if os.path.exists("score.txt"):
        with open("score.txt", "rt", encoding='utf-8') as f:
            while f.readline():
                self.score.append(int(f.readline()))
                break
        print(self.score)
        messagebox.showinfo('점수',self.score)

    def create_button(self):
        button = tk.Button(self, text='New Game', command=lambda: self.new_game())
        button1 = tk.Button(self, text='Scores', command=lambda : self.get_score())
        button.place(relx=0.1, rely=0.10, anchor="center")
        button1.place(relx=0.1, rely=0.17, anchor="center")

    def new_game(self):
        self.make_GUI()
        self.start_game()

    def start_game(self):
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=CELL_COLORS[2],
            fg=CELL_NUMBER_COLORS[2],
            font=CELL_NUMBER_FONTS,
            text="2"
        )
        while (self.matrix[row][col] != 0):
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=CELL_COLORS[2],
            fg=CELL_NUMBER_COLORS[2],
            font=CELL_NUMBER_FONTS,
            text="2"
        )

    def stack(self):
        new_matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            fill_position = 0
            for col in range(self.grid_size):
                if self.matrix[row][col] != 0:
                    new_matrix[row][fill_position] = self.matrix[row][col]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size-1):
                if (self.matrix[row][col] != 0) and (self.matrix[row][col] == self.matrix[row][col + 1]):
                    self.matrix[row][col] *= 2
                    self.matrix[row][col + 1] = 0
                    self.score += self.matrix[row][col]
                    if self.score > self.bstScore:
                        self.bstScore = self.score
                        with open("bestscore.txt", "w") as f:
                            f.write(str(self.bstScore))



    def reverse(self):
        new_matrix = []
        for row in range(self.grid_size):
            new_matrix.append([])
            for col in range(self.grid_size):
                new_matrix[row].append(self.matrix[row][(self.grid_size-1) - col])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0]*self.grid_size for _ in range(self.grid_size)]
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                new_matrix[row][col] = self.matrix[col][row]
        self.matrix = new_matrix

    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0,self.grid_size-1)
            col = random.randint(0,self.grid_size-1)
            while(self.matrix[row][col] != 0):
                row = random.randint(0,self.grid_size-1)
                col = random.randint(0,self.grid_size-1)
            self.matrix[row][col] = random.choice([2, 4])

    def update_GUI(self):
        cell_text_color = 0
        cell_cell_color = 0
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell_value = self.matrix[row][col]
                if cell_value == 0:
                    self.cells[row][col]["frame"].configure(bg=EMPTY_CELL_COLOR)
                    self.cells[row][col]["number"].configure(bg=EMPTY_CELL_COLOR, text="")
                else:
                    if cell_value >= 8:
                        cell_text_color = 8
                    else:
                        cell_text_color = cell_value
                    if cell_value >= 4096:
                        cell_cell_color = 4096
                    else:
                        cell_cell_color = cell_value

                    self.cells[row][col]["frame"].configure(bg=CELL_COLORS[cell_cell_color])
                    self.cells[row][col]["number"].configure(
                        bg=CELL_COLORS[cell_cell_color],
                        fg=CELL_NUMBER_COLORS[cell_text_color],
                        font=CELL_NUMBER_FONTS,
                        text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.record_label.configure(text=self.bstScore)
        self.update_idletasks()

    def any_move(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size-1):
                if self.matrix[i][j] == self.matrix[i][j + 1] or \
                   self.matrix[j][i] == self.matrix[j + 1][i] :
                    return True
        return False

    def game_over(self):
        # Check if tovalue is reached
        if any(self.top_value in row for row in self.matrix):
            text = f"You did {self.top_value}!!"
            self.popup(text, text + " Cotinue?")
            self.top_value = self.top_value*2
        # Check if there are no more moves in the grid
        elif not any(0 in row for row in self.matrix) and not self.any_move():
            self.popup("Game Over!!", "Game Over!!")
            with open("score.txt", "at", encoding='utf-8') as f:
                f.writelines(str(self.score)+"\n")

    def popup (self, win_title, win_message):
        popup_win = tk.Toplevel()
        popup_win.wm_title(win_title)
        w = 200
        h = 50
        x = (self.sw - w)/2
        y = (self.sh - h)/2
        popup_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
        l = tk.Label(popup_win, text=win_message)
        l.grid(row=0, column=0)
        b = tk.Button(popup_win, text="Ok", command=popup_win.destroy)
        b.grid(row=1, column=0)

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()



    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

# if __name__ == "__main__":
#     Game()