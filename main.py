import threading
import tkinter as tk
import time
from agents.agent_random import RandomAgent
from agents.agent_minimax import MinimaxAgent
from agents.agent_carlo import CarloAgent
from agents.agent_probcut import ProbCutAgent
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

    # RandomAgent() - Igra random poteze
    # MinimaxAgent(dubina) - Igra sa zadatom dubinom
    # CarloAgent(br_simulacija, exploration_factor) - Igra pomocu monte karlo pretrage sa datim brojem simulacija i sa datim faktorom istrazivanja

    # Ukoliko je igrac protiv agenta koristiti poziv linije 28
    # game.set_player(MinimaxAgent(2))

    # Ukoliko je agent prtiv agenta korisitit poziv linije 31
    # game.set_players(ProbCutAgent(2), ProbCutAgent(3))
    game.set_players(MinimaxAgent(2), MinimaxAgent(3))

    root.mainloop()

