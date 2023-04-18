import random
from agents.agent import Agent

class RandomAgent(Agent):

    def make_move(self) -> (int, int):
        moves = self.game.find_all_legal_moves(self.turn)
        if not moves:
            return None
        move = random.choice(moves)
        return move
