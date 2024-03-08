import tkinter as tk
import random
from tkinter import messagebox


class GameBoard(tk.Tk):
    def __init__(self, rows=10, cols=10, size=50):
        super().__init__()
        self.title("Le monde en noir et blanc")

        self.rows = rows
        self.cols = cols
        self.size = size
        self.time_limit= 10000 # 10s
        self.game_over = False

        self.canvas = tk.Canvas(self, width=cols*size, height=rows*size)
        self.canvas.pack()

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.game_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Game", menu=self.game_menu)
        self.game_menu.add_command(label="Restart", command=self.restart_game)

        self.character_img = tk.PhotoImage(file="perso.png")
        self.goal_img = tk.PhotoImage(file="goal.png")
        self.goal_pos = (0,0)
        self.character_pos = (0, 0)
        self.board = []

        self.generate_new_board()
        self.bind("<KeyPress>", self.on_key_press)
        self.start_timer()

    def draw_board(self):
        self.canvas.delete("all")  
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.board[row][col]
                x1, y1 = col * self.size, row * self.size
                x2, y2 = x1 + self.size, y1 + self.size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="gray")
        self.draw_character()
        self.draw_goal()

    def draw_goal(self):
        x, y = self.goal_pos
        self.canvas.create_image(x * self.size + self.size//2, y * self.size + self.size//2, image=self.goal_img)
    

    def draw_character(self):
        x, y = self.character_pos
        self.canvas.create_image(x * self.size + self.size//2,
                                 y * self.size + self.size//2, image=self.character_img)

    def on_key_press(self, event):
        if not self.game_over:
            x, y = self.character_pos
            if self.board[y][x] == "black":
                if event.keysym == "Right":
                    x += 1
                elif event.keysym == "Left":
                    x -= 1
                elif event.keysym == "Up":
                    y -= 1
                elif event.keysym == "Down":
                    y += 1
            else: 
                if event.keysym == "Right":
                    x -= 1
                elif event.keysym == "Left":
                    x += 1
                elif event.keysym == "Up":
                    y += 1
                elif event.keysym == "Down":
                    y -= 1

            if 0 <= x < self.cols and 0 <= y < self.rows:  
                self.character_pos = (x, y)
                self.draw_board()

    def generate_new_board(self):
        self.board = [["white" if random.choice(
            [True, False]) else "black" for _ in range(self.cols)] for _ in range(self.rows)]
        self.character_pos = (0, 0)
        self.set_goal_position()
        self.draw_board()

    def set_goal_position(self):
        if random.choice([True, False]):
            self.goal_pos = (random.randint(0, self.cols - 1), self.rows - 1)
        else:
            self.goal_pos = (self.cols - 1, random.randint(0, self.rows - 1))

    def start_timer(self):
        self.after(self.time_limit, self.time_is_up)

    def time_is_up(self):
        if not self.game_over:
            self.game_over = True
            messagebox.showinfo("Game Over", "Time's up! You didn't reach the goal.")
            self.game_menu.add_command(label="Restart", command=self.restart_game)
    

    def restart_game(self):
        self.game_over = False
        self.generate_new_board()
        self.start_timer()


if __name__ == "__main__":
    game = GameBoard()
    game.mainloop()
