import threading
import time
import tkinter as tk
from tkinter import messagebox
from agents.agent import Agent
from board import Board, BLACK, WHITE, MOVE, ROWS, COLS
from agents.agent_expectimax import ExpectimaxAgent
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_carlo import CarloAgent
from agents.agent_probcut import ProbCutAgent

FIELD_SIZE = 70

class Game:

    def __init__(self, master, turn: str):
        self.turn = turn
        self.board = Board(turn)
        self.master = master
        self.thread = None
        self.__init_gui(self.master)
        self.white: Agent | None = None
        self.black: Agent | None = None
        self.game_over: bool = False
        self.game_no: int = 0

    def set_player(self, agent: Agent):
        agent.init(self.board, BLACK)
        self.black = agent

    def set_players(self, agent_one: Agent, agent_two: Agent):
        agent_one.init(self.board, WHITE)
        self.white = agent_one
        self.set_player(agent_two)

    def stop_game(self):
        self.game_over = True
        self.turn = WHITE
        self.board = Board(self.turn)
        self.__draw_board()

    def start_simulation(self):
        self.game_no += 1
        self.game_over = False
        self.thread = threading.Thread(target=self.__simulation, args=(self.game_no, ))
        self.thread.start()

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

        # Options buttons
        self.options_frame = tk.Frame(master, bg="#353535", padx=10, pady=10)
        self.options_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.reset_button = tk.Button(self.options_frame, text="RESET GAME", bg="#353535", fg="white", padx=4, pady=4, command=self.__reset_game)
        self.reset_button.pack(side=tk.LEFT)
        self.settings_button = tk.Button(self.options_frame, text="SETTINGS", bg="#353535", fg="white", padx=4, pady=4, command=self.__open_settings)
        self.settings_button.pack(side=tk.RIGHT)

        self.__draw_board()

        self.canvas.bind("<Button-1>", self.__handle_click)

    def __handle_click(self, event):
        if self.white is not None or self.turn is not WHITE:
            return
        row, col = event.y // FIELD_SIZE, event.x // FIELD_SIZE
        self.__make_a_move(row, col, WHITE)

    def __reset_game(self):
        self.stop_game()
        if self.white is not None:
            self.white.init(self.board, WHITE)
        if self.black is not None:
            self.black.init(self.board, BLACK)
        self.game_over = False
        if self.thread is not None:
            self.start_simulation()

    def  __open_settings(self):
        self.settings_window = tk.Toplevel(self.master, padx=80, pady=40)
        self.settings_window.title("Settings")

        def callback1(*args):
            if self.player1.get() == "Human" or self.player1.get() == "Random":
                depth1_label.grid_forget()
                depth1_dropdown.grid_forget()
                simulation1_label.grid_forget()
                simulation1_dropdown.grid_forget()
                exploration1_label.grid_forget()
                exploration1_dropdown.grid_forget()
                probcut1_label.grid_forget()
                probcut1_dropdown.grid_forget()
            elif self.player1.get() == "Minimax" or self.player1.get() == "Expectimax":
                depth1_label.grid(row=1, column=0)
                depth1_dropdown.grid(row=1, column=1, padx=10, pady=10)
                simulation1_label.grid_forget()
                simulation1_dropdown.grid_forget()
                exploration1_label.grid_forget()
                exploration1_dropdown.grid_forget()
                probcut1_label.grid_forget()
                probcut1_dropdown.grid_forget()
            elif self.player1.get() == "Monte Carlo":
                depth1_label.grid_forget()
                depth1_dropdown.grid_forget()
                simulation1_label.grid(row=1, column=0)
                simulation1_dropdown.grid(row=1, column=1, padx=10, pady=10)
                exploration1_label.grid(row=2, column=0)
                exploration1_dropdown.grid(row=2, column=1, padx=10, pady=10)
                probcut1_label.grid_forget()
                probcut1_dropdown.grid_forget()
            elif self.player1.get() == "ProbCut":
                depth1_label.grid(row=1, column=0)
                depth1_dropdown.grid(row=1, column=1, padx=10, pady=10)
                simulation1_label.grid_forget()
                simulation1_dropdown.grid_forget()
                exploration1_label.grid_forget()
                exploration1_dropdown.grid_forget()
                probcut1_label.grid(row=2, column=0)
                probcut1_dropdown.grid(row=2, column=1, padx=10, pady=10)

        def callback2(*args):
            if self.player2.get() == "Human" or self.player2.get() == "Random":
                depth2_label.grid_forget()
                depth2_dropdown.grid_forget()
                simulation2_label.grid_forget()
                simulation2_dropdown.grid_forget()
                exploration2_dropdown.grid_forget()
                exploration2_label.grid_forget()
                probcut2_label.grid_forget()
                probcut2_dropdown.grid_forget()
            elif self.player2.get() == "Minimax" or self.player2.get() == "Expectimax":
                depth2_label.grid(row=1, column=2)
                depth2_dropdown.grid(row=1, column=3, padx=10, pady=10)
                simulation2_label.grid_forget()
                simulation2_dropdown.grid_forget()
                exploration2_label.grid_forget()
                exploration2_dropdown.grid_forget()
                probcut2_label.grid_forget()
                probcut2_dropdown.grid_forget()
            elif self.player2.get() == "Monte Carlo":
                depth2_label.grid_forget()
                depth2_dropdown.grid_forget()
                simulation2_label.grid(row=1, column=2)
                simulation2_dropdown.grid(row=1, column=3, padx=10, pady=10)
                exploration2_label.grid(row=2, column=2)
                exploration2_dropdown.grid(row=2, column=3, padx=10, pady=10)
                probcut2_label.grid_forget()
                probcut2_dropdown.grid_forget()
            elif self.player2.get() == "ProbCut":
                depth2_label.grid(row=1, column=2)
                depth2_dropdown.grid(row=1, column=3, padx=10, pady=10)
                simulation2_label.grid_forget()
                simulation2_dropdown.grid_forget()
                exploration2_label.grid_forget()
                exploration2_dropdown.grid_forget()
                probcut2_label.grid(row=2, column=2)
                probcut2_dropdown.grid(row=2, column=3, padx=10, pady=10)

        player1_options = ["Human", "Minimax", "Monte Carlo", "Expectimax", "ProbCut", "Random"]
        self.player1 = tk.StringVar(self.master)
        self.player1.set(player1_options[0])
        self.player1.trace("w", callback1)
        player2_options = ["Minimax", "Monte Carlo", "Expectimax", "ProbCut", "Random"]
        self.player2 = tk.StringVar(self.master)
        self.player2.set(player2_options[0])
        self.player2.trace("w", callback2)

        # Create the dropdowns for selecting players
        player1_label = tk.Label(self.settings_window, text="White Player:")
        player1_label.grid(row=0, column=0)
        player1_dropdown = tk.OptionMenu(self.settings_window, self.player1, *player1_options)
        player1_dropdown.grid(row=0, column=1, padx=10, pady=10)

        player2_label = tk.Label(self.settings_window, text="Black Player:")
        player2_label.grid(row=0, column=2)
        player2_dropdown = tk.OptionMenu(self.settings_window, self.player2, *player2_options)
        player2_dropdown.grid(row=0, column=3, padx=10, pady=10)

        # Depth Selection
        depth_options = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.depth1 = tk.StringVar(self.master)
        self.depth1.set(depth_options[0])
        self.depth2 = tk.StringVar(self.master)
        self.depth2.set(depth_options[0])

        depth1_label = tk.Label(self.settings_window, text="Depth:")
        depth1_dropdown = tk.OptionMenu(self.settings_window, self.depth1, *depth_options)
        depth2_label = tk.Label(self.settings_window, text="Depth:")
        depth2_label.grid(row=1, column=2)
        depth2_dropdown = tk.OptionMenu(self.settings_window, self.depth2, *depth_options)
        depth2_dropdown.grid(row=1, column=3, padx=10, pady=10)

        # Simulations Selection
        simulation_options = ["50", "100", "200", "300", "400", "500", "600", "800"]
        self.simulation1 = tk.StringVar(self.master)
        self.simulation1.set(simulation_options[0])
        self.simulation2 = tk.StringVar(self.master)
        self.simulation2.set(simulation_options[0])

        simulation1_label = tk.Label(self.settings_window, text="Simulations:")
        simulation1_dropdown = tk.OptionMenu(self.settings_window, self.simulation1, *simulation_options)
        simulation2_label = tk.Label(self.settings_window, text="Simulations:")
        simulation2_dropdown = tk.OptionMenu(self.settings_window, self.simulation2, *simulation_options)

        # Explaration Selection
        exploration_options = ["0.9", "1.2", "1.5", "1.8", "2.1", "2.4", "2.7", "3.0"]
        self.exploration1 = tk.StringVar(self.master)
        self.exploration1.set(exploration_options[0])
        self.exploration2 = tk.StringVar(self.master)
        self.exploration2.set(exploration_options[0])

        exploration1_label = tk.Label(self.settings_window, text="Exploration:")
        exploration1_dropdown = tk.OptionMenu(self.settings_window, self.exploration1, *exploration_options)
        exploration2_label = tk.Label(self.settings_window, text="Exploration:")
        exploration2_dropdown = tk.OptionMenu(self.settings_window, self.exploration2, *exploration_options)

        # Delta Selection
        delta_options = ["0.4", "0.6", "0.8", "1.0", "1.2", "1.4", "1.5", "1.6", "1.8", "2.0", "2.2"]
        self.probcut1 = tk.StringVar(self.master)
        self.probcut1.set(delta_options[0])
        self.probcut2 = tk.StringVar(self.master)
        self.probcut2.set(delta_options[0])

        probcut1_label = tk.Label(self.settings_window, text="Probcut:")
        probcut1_dropdown = tk.OptionMenu(self.settings_window, self.probcut1, *delta_options)
        probcut2_label = tk.Label(self.settings_window, text="Probcut:")
        probcut2_dropdown = tk.OptionMenu(self.settings_window, self.probcut2, *delta_options)

        # OK Button
        button = tk.Button(self.settings_window, text="OK", padx=18, pady=4, command=self.__confirm)
        button.grid(row=5, column=3, padx=10, pady=10)

    def __confirm(self):
        self.stop_game()

        player1 = None
        player2 = None

        if self.player1.get() == "Random":
            player1 = RandomAgent()
        elif self.player1.get() == "Minimax":
            player1 = MinimaxAgent(int(self.depth1.get()))
        elif self.player1.get() == "Monte Carlo":
            player1 = CarloAgent(int(self.simulation1.get()), float(self.exploration1.get()))
        elif self.player1.get() == "Expectimax":
            player1 = ExpectimaxAgent(int(self.depth1.get()))
        elif self.player1.get() == "ProbCut":
            player1 = ProbCutAgent(int(self.depth1.get()), float(self.probcut1.get()))

        if self.player2.get() == "Random":
            player2 = RandomAgent()
        elif self.player2.get() == "Minimax":
            player2 = MinimaxAgent(int(self.depth2.get()))
        elif self.player2.get() == "Monte Carlo":
            player2 = CarloAgent(int(self.simulation2.get()), float(self.exploration2.get()))
        elif self.player2.get() == "Expectimax":
            player2 = ExpectimaxAgent(int(self.depth2.get()))
        elif self.player2.get() == "ProbCut":
            player2 = ProbCutAgent(int(self.depth2.get()), float(self.probcut2.get()))

        if player1 is not None and player2 is not None:
            self.stop_game()
            self.set_players(player1, player2)
            self.start_simulation()
        elif player2 is not None:
            self.stop_game()
            self.white = None
            self.set_player(player2)

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

    def __simulation(self, no: int):
        print(no)
        while not self.game_over and no == self.game_no:
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
