import threading
import time
import tkinter as tk
from tkinter import messagebox
from agents.agent import Agent
from board import Board, BLACK, WHITE, MOVE, ROWS, COLS


class Game:

    def __init__(self, master):
        self.game = Board(WHITE)
        self.master = master
        self.__init_gui(self.master)
        self.white: Agent | None = None
        self.black: Agent | None = None
        self.game_over: bool = False

    def set_player(self, agent: Agent):
        agent.init(self.game, BLACK)
        self.black = agent

    def set_players(self, agent_one: Agent, agent_two: Agent):
        agent_one.init(self.game, WHITE)
        self.white = agent_one
        self.set_player(agent_two)

        thread = threading.Thread(target=self.__simulation)
        thread.start()

    def __init_gui(self, master):
        master.title("Othello")
        master.resizable(False, False)

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

        self.__draw_board()

        self.canvas.bind("<Button-1>", self.__handle_click)

    def __handle_click(self, event):
        if self.white is not None or self.game.turn is not WHITE:
            return
        row, col = event.y // 50, event.x // 50
        self.__make_a_move(row, col)

    def __make_a_move(self, row, col):
        if self.game.move(row, col):
            self.__draw_board()
            if self.game.is_game_over():
                self.game_over = True
                self.__finish_game()
            elif self.white is None and self.black is not None and self.game.turn == BLACK:
                t = threading.Thread(target=self.__black_plays)
                t.start()

    def __black_plays(self):
        time.sleep(0.25)
        self.__make_a_move(*self.black.make_move())

    def __simulation(self):
        while not self.game_over:
            # time.sleep(0.05)
            white_move = self.white.make_move()
            if white_move:
                self.__make_a_move(*white_move)

            # time.sleep(0.05)
            black_move = self.black.make_move()
            if black_move:
                self.__make_a_move(*black_move)

    def __draw_board(self):
        self.canvas.delete(tk.ALL)

        # Draw the cells of the board
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * 50
                y1 = row * 50
                x2 = x1 + 50
                y2 = y1 + 50
                color = "#eeeeee" if (row + col) % 2 == 0 else "#f8f8f8"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#eee")

        # Draw the pieces on the board
        board = self.game.get_board()
        for row in range(ROWS):
            for col in range(COLS):
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

    def __finish_game(self):
        winner = self.game.return_winner()
        if winner:
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

    @staticmethod
    def __write_move_to_file(row: int, col: int):
        with open("debug_moves.txt", "a") as f:
            f.write("{},{}/n".format(row, col))
