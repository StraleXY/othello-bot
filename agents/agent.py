from abc import ABC, abstractmethod
from game import Game


class Agent(ABC):

    def __init__(self):
        self.turn = ''
        self.game = None

    def init(self, game: Game, turn: str):
        self.turn = turn
        self.game = game

    @abstractmethod
    def make_move(self):
        pass
