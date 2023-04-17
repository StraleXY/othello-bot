from game import Game

import tkinter as tk
from game import Game

class ReversiGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Othello")
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.game = Game('W')
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="dark green")

                if self.game.board[row][col] == 'B':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")
                elif self.game.board[row][col] == 'W':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")

    def handle_click(self, event):
        col = event.x // 50
        row = event.y // 50
        if self.game.is_valid_move(row, col, self.game.turn):
            self.game.move(row, col)
            self.draw_board()

            if self.game.is_game_over():
                self.show_winner()
            else:
                if not self.game.has_legal_moves(self.game.turn):
                    self.game.turn = self.game.opposite_turn(self.game.turn)
                    if not self.game.has_legal_moves(self.game.turn):
                        self.show_winner()

    def show_winner(self):
        black_count = sum(row.count('B') for row in self.game.board)
        white_count = sum(row.count('W') for row in self.game.board)
        if black_count > white_count:
            winner = "Black"
        elif white_count > black_count:
            winner = "White"
        else:
            winner = "Tie"
        self.canvas.create_text(200, 200, text=f"{winner} wins!", font=("Arial", 24))

if __name__ == '__main__':
    root = tk.Tk()
    game_gui = ReversiGUI(master=root)
    game_gui.mainloop()


# if __name__ == '__main__':
#     game = Game('W')
#     game.print_board()
#     while True:
#         print(game.get_turn())
#         input_str = input("Enter move coordinates (row, col): ")
#         x, y = map(int, input_str.split(","))
#         game.move(x, y)
#         game.print_board()