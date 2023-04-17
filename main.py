import tkinter as tk
from tkinter import messagebox
from game import Game, BLACK, WHITE


class GameGUI:

    def __init__(self, master):
        self.master = master
        master.title("Othello")

        self.game = Game(BLACK)

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

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
                color = "#0B6623" if (row + col) % 2 == 0 else "#3CB371"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

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

    def handle_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if self.game.move(row, col):
            self.game.print_board()
            self.draw_board()
            if self.game.is_game_over():
                winner = self.game.return_winner()
                if winner:
                    messagebox.showinfo("Game Over", f"The winner is {winner}!")
                else:
                    messagebox.showinfo("Game Over", "It's a tie!")


if __name__ == "__main__":
    root = tk.Tk()
    messagebox.showinfo("Game Over", "It's a tie!")
    game_gui = GameGUI(root)
    root.mainloop()
