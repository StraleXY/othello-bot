import threading
import tkinter as tk
import time
from agents.agent_random import RandomAgent
from gui import GameGUI


# def debug():
#     with open('debug_moves.txt', 'r') as f:
#         for line in f:
#             x, y = line.strip().split(',')
#             game_gui.__make_a_move(int(x), int(y))
#             time.sleep(0.1)


if __name__ == "__main__":
    root = tk.Tk()
    game_gui = GameGUI(root)
    game_gui.set_players(RandomAgent(), RandomAgent())
    root.mainloop()

