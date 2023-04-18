import tkinter as tk
from tkinter import messagebox
from game import Game, BLACK, WHITE, EMPTY, MOVE
import threading
import time


class GameGUI:

    def __init__(self, master):
        self.master = master
        master.title("Othello")
        master.resizable(False, False)

        self.game = Game(BLACK)

        # Show score
        self.score_frame = tk.Frame(master, bg="#353535")
        self.score_frame.pack(side=tk.TOP, fill=tk.X)
        self.black_score_label = tk.Label(self.score_frame, text=f"Black: 3", fg="white", bg="#353535", font=("Arial", 18))
        self.black_score_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.white_score_label = tk.Label(self.score_frame, text=f"White: 2", fg="white", bg="#353535", font=("Arial", 18))
        self.white_score_label.pack(side=tk.RIGHT, padx=20, pady=10)

        # Show board
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Show current player
        self.current_player_label = tk.Label(master, text=f"Current player: {BLACK}", font=("Arial", 13), bg="#353535", fg="white", pady=8)
        self.current_player_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.draw_board()

        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        self.canvas.delete(tk.ALL)
        rows = self.game.get_rows()
        cols = self.game.get_cols()

        # Draw the cells of the board
        for row in range(rows):
            for col in range(cols):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "#eeeeee" if (row + col) % 2 == 0 else "#f8f8f8"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#eee")

        # Draw the pieces on the board
        board = self.game.get_board()
        for row in range(rows):
            for col in range(cols):
                x = col * 50 + 25
                y = row * 50 + 25
                if board[row][col] == BLACK:
                    self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="black")
                elif board[row][col] == WHITE:
                    self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white")
                elif board[row][col] == MOVE:
                    self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="#FFFCDB", outline="#DFDDBF")

        # Update the current player label
        self.current_player_label.config(text=f"Current player: {self.game.turn}")
        self.black_score_label.config(text=f"Black: {self.game.get_cells_count(BLACK)}")
        self.white_score_label.config(text=f"White: {self.game.get_cells_count(WHITE)}")

    def handle_click(self, event):
        col = event.x // 50
        row = event.y // 50
        self.make_a_move(row, col)

        # with open("debug_moves.txt", "a") as f:
        #     f.write("{},{}/n".format(row, col))

    def make_a_move(self, row, col):
        if self.game.move(row, col):
            self.game.print_board()
            self.draw_board()
            if self.game.is_game_over():
                winner = self.game.return_winner()
                if winner:
                    messagebox.showinfo("Game Over", f"The winner is {winner}!")
                else:
                    messagebox.showinfo("Game Over", "It's a tie!")


def debug():
    with open('debug_moves.txt', 'r') as f:
        for line in f:
            x, y = line.strip().split(',')
            game_gui.make_a_move(int(x), int(y))
            time.sleep(0.1)


if __name__ == "__main__":
    root = tk.Tk()
    game_gui = GameGUI(root)
    # Debug mode
    # t = threading.Thread(target=debug)
    # t.start()
    root.mainloop()

