import threading
import tkinter as tk
import time
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent
from game import Game
from board import WHITE


# def debug():
#     with open('debug_moves.txt', 'r') as f:
#         for line in f:
#             x, y = line.strip().split(',')
#             game_gui.__make_a_move(int(x), int(y))
#             time.sleep(0.1)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root, WHITE)
    # game.set_player(MinimaxAgent(3))
    game.set_players(MinimaxAgent(4), MinimaxAgent(2))
    root.mainloop()

