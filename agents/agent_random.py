import random
from agents.agent import Agent

class RandomAgent(Agent):

    def make_move(self) -> (int, int):
        # self.game.remove_pieces('x')
        print(self.game.find_all_legal_moves(self.turn))
        move = random.choice(self.game.find_all_legal_moves(self.turn))
        print(move)
        return move
