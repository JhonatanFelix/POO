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
        self.time_limit = 10  # 10 segundos
        self.timer_text = tk.StringVar()
        self.game_over = False

        self.canvas = tk.Canvas(self, width=cols*size, height=rows*size)
        self.canvas.pack()

        self.timer_label = tk.Label(self, textvariable=self.timer_text)
        self.timer_label.pack()

        self.character_img = tk.PhotoImage(file="tk_cours\perso.png")
        self.goal_img = tk.PhotoImage(file="tk_cours\goal.png")
        self.character_pos = (0, 0)
        self.goal_pos = (0, 0)
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

    def draw_character(self):
        x, y = self.character_pos
        self.canvas.create_image(x * self.size + self.size//2,
                                 y * self.size + self.size//2, image=self.character_img)

    def draw_goal(self):
        x, y = self.goal_pos
        self.canvas.create_image(
            x * self.size + self.size//2, y * self.size + self.size//2, image=self.goal_img)

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

            if 0 <= x < self.cols and 0 <= y < self.rows:  # Verifica se está dentro dos limites
                self.character_pos = (x, y)
                self.check_goal_reached()
                self.draw_board()

    def check_goal_reached(self):
        if self.character_pos == self.goal_pos:
            self.game_over = True
            messagebox.showinfo("Congratulations!",
                                "You've reached the goal and won the game!")
            self.restart_game()

    def generate_new_board(self):
        self.board = [["white" if random.choice(
            [True, False]) else "black" for _ in range(self.cols)] for _ in range(self.rows)]
        self.set_goal_position()
        self.character_pos = (0, 0)
        self.game_over = False
        self.draw_board()

    def set_goal_position(self):
        if random.choice([True, False]):
            self.goal_pos = (random.randint(0, self.cols - 1), self.rows - 1)
        else:
            self.goal_pos = (self.cols - 1, random.randint(0, self.rows - 1))

    def start_timer(self):
        self.update_timer()

    def update_timer(self):
        if self.time_limit > 0 and not self.game_over:
            self.timer_text.set(f"Time left: {self.time_limit} seconds")
            self.time_limit -= 1
            # Chama a si mesmo a cada 1 segundo
            self.after(1000, self.update_timer)
        elif self.time_limit == 0:
            self.time_is_up()

    def time_is_up(self):
        if not self.game_over:
            self.game_over = True
            response = messagebox.askyesno(
                "Game Over", "Time's up! You didn't reach the goal. Do you want to restart?")
            if response:
                self.restart_game()
            else:
                self.quit()  

    def restart_game(self):
        self.time_limit = 10  # Reset o timer para 10 segundos
        self.game_over = False
        self.generate_new_board()
        self.start_timer()


if __name__ == "__main__":
    game = GameBoard()
    game.mainloop()
