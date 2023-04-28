import threading
import time
import tkinter as tk
from tkinter import messagebox
from agents.agent import Agent
from board import Board, BLACK, WHITE, MOVE, ROWS, COLS

FIELD_SIZE = 70

class Game:

    def __init__(self, master, turn: str):
        self.turn = turn
        self.board = Board(turn)
        self.master = master
        self.__init_gui(self.master)
        self.white: Agent | None = None
        self.black: Agent | None = None
        self.game_over: bool = False

    def set_player(self, agent: Agent):
        agent.init(self.board, BLACK)
        self.black = agent

    def set_players(self, agent_one: Agent, agent_two: Agent):
        agent_one.init(self.board, WHITE)
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
        self.white_score_label = tk.Label(self.score_frame, text=f"White: 2", fg="white", bg="#353535", font=("Arial", 18))
        self.white_score_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.black_score_label = tk.Label(self.score_frame, text=f"Black: 3", fg="white", bg="#353535", font=("Arial", 18))
        self.black_score_label.pack(side=tk.RIGHT, padx=20, pady=10)

        # Show board
        self.canvas = tk.Canvas(master, width=FIELD_SIZE*COLS, height=FIELD_SIZE*ROWS)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Show current player
        self.current_player_label = tk.Label(master, text=f"Current player: {BLACK}", font=("Arial", 13), bg="#353535", fg="white", pady=8)
        self.current_player_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.__draw_board()

        self.canvas.bind("<Button-1>", self.__handle_click)

    def __handle_click(self, event):
        if self.white is not None or self.turn is not WHITE:
            return
        row, col = event.y // FIELD_SIZE, event.x // FIELD_SIZE
        self.__make_a_move(row, col, WHITE)

    def __make_a_move(self, row, col, turn):
        result = self.board.move(row, col, turn)
        if result[0]:
            self.turn = result[1]
            self.__draw_board()
            if self.board.is_game_over():
                self.game_over = True
                self.__finish_game()
            elif self.white is None and self.black is not None and self.turn == BLACK:
                t = threading.Thread(target=self.__black_plays)
                t.start()

    def __black_plays(self):
        time.sleep(0.25)
        self.__make_a_move(*self.black.make_move(), BLACK)

    def __simulation(self):
        while not self.game_over:
            if self.turn == WHITE:
                white_move = self.white.make_move()
                if white_move:
                    self.__make_a_move(*white_move, WHITE)

            if self.turn == BLACK:
                black_move = self.black.make_move()
                if black_move:
                    self.__make_a_move(*black_move, BLACK)

    def __draw_board(self):
        self.canvas.delete(tk.ALL)

        # Draw the cells of the board
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * FIELD_SIZE
                y1 = row * FIELD_SIZE
                x2 = x1 + FIELD_SIZE
                y2 = y1 + FIELD_SIZE
                color = "#eeeeee" if (row + col) % 2 == 0 else "#f8f8f8"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#eee")

        # Draw the pieces on the board
        board = self.board.get_board()
        disk_offset = FIELD_SIZE / 2 - 8
        for row in range(ROWS):
            for col in range(COLS):
                x = col * FIELD_SIZE + (FIELD_SIZE / 2)
                y = row * FIELD_SIZE + (FIELD_SIZE / 2)
                if board[row][col] == BLACK:
                    self.canvas.create_oval(x - disk_offset, y - disk_offset, x + disk_offset, y + disk_offset, fill="black")
                elif board[row][col] == WHITE:
                    self.canvas.create_oval(x - disk_offset, y - disk_offset, x + disk_offset, y + disk_offset, fill="white")
                elif board[row][col] == MOVE:
                    self.canvas.create_oval(x - disk_offset, y - disk_offset, x + disk_offset, y + disk_offset, fill="#FFFCDB", outline="#DFDDBF")

        # Update the current player label
        self.current_player_label.config(text=f"Current player: {self.turn}")
        self.black_score_label.config(text=f"Black: {self.board.get_cells_count(BLACK)}")
        self.white_score_label.config(text=f"White: {self.board.get_cells_count(WHITE)}")

    def __finish_game(self):
        winner = self.board.return_winner()
        if winner:
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")

    @staticmethod
    def __write_move_to_file(row: int, col: int):
        with open("debug_moves.txt", "a") as f:
            f.write("{},{}/n".format(row, col))
