import tkinter as tk
import random

class SnakeGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.game_speed = 100
        self.init_game()
        self.pack()

    def init_game(self):
        self.direction = "Right"
        self.next_direction = self.direction
        self.score = 0
        self.food_consumed = 0
        self.game_running = True
        self.snake = [(self.width // 2, self.height // 2)]
        self.food_position = self.place_food()
        self.master.bind("<Key>", self.change_direction)
        self.master.bind("<space>", self.toggle_pause)
        self.create_widgets()
        self.update_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        self.score_label = tk.Label(self, text=f"Score: {self.score}")
        self.score_label.pack()
        self.restart_button = tk.Button(self, text="Restart", command=self.restart_game)
        self.restart_button.pack_forget()  # Initially hide the restart button
        self.draw_snake()
        self.draw_food()

    def restart_game(self):
        self.canvas.delete("all")
        self.score_label.pack_forget()
        self.restart_button.pack_forget()
        self.init_game()

    def toggle_pause(self, event):
        if self.game_running:
            self.game_running = False
        else:
            self.game_running = True
            self.update_game()

    def place_food(self):
        while True:
            position = (random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size,
                        random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size)
            if position not in self.snake:
                return position

    def draw_snake(self):
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + self.cell_size, segment[1] + self.cell_size, fill="green", tags="snake")

    def draw_food(self):
        self.canvas.create_rectangle(self.food_position[0], self.food_position[1], self.food_position[0] + self.cell_size, self.food_position[1] + self.cell_size, fill="red", tags="food")

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.next_direction == "Left":
            head_x -= self.cell_size
        elif self.next_direction == "Right":
            head_x += self.cell_size
        elif self.next_direction == "Up":
            head_y -= self.cell_size
        elif self.next_direction == "Down":
            head_y += self.cell_size
        new_head = (head_x, head_y)
        return new_head

    def update_game(self):
        if self.game_running:
            new_head = self.move_snake()
            if self.check_collisions(new_head):
                self.game_over()
                return
            self.snake.insert(0, new_head)
            if new_head == self.food_position:
                self.score += 10
                self.food_consumed += 1
                self.score_label.config(text=f"Score: {self.score}")
                self.food_position = self.place_food()
                self.canvas.delete("food")
                self.draw_food()
                if self.food_consumed % 5 == 0:
                    self.game_speed = max(10, self.game_speed - 10)
            else:
                tail = self.snake.pop()
                self.canvas.delete(self.canvas.find_closest(tail[0] + self.cell_size // 2, tail[1] + self.cell_size // 2))
            self.direction = self.next_direction
            self.canvas.delete("snake")
            self.draw_snake()
            self.master.after(self.game_speed, self.update_game)

    def check_collisions(self, position):
        x, y = position
        if x < 0 or x >= self.width or y < 0 or y >= self.height or position in self.snake:
            return True
        return False

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.next_direction = event.keysym

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(self.width // 2, self.height // 2, text="GAME OVER", font=("Arial", 24, "bold"), fill="red")
        self.score_label.config(text=f"Game Over! Score: {self.score}")
        self.restart_button.pack()

root = tk.Tk()
root.title("Snake Game")
app = SnakeGame(master=root)
app.mainloop()
