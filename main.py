import tkinter
import tkinter as tk

from Tools.scripts.serve import app

root = tk.Tk()
root.title("뽀글뽀글 미니게임")
root.geometry("900x900")
wall = tkinter.PhotoImage(file="1.gif")
wall_label = tkinter.Label(image=wall)
wall_label.place(x=0, y=0)

btn = tkinter.Button(root, padx=5, pady=10, text="press start")
# btn.pack(ipadx=50, padx=60)
btn.place(x=295,y=650,width = 350, height=60)


root.resizable(True, False)
root.mainloop()
