from abc import ABC, abstractmethod
from board import Board


class Agent(ABC):

    def __init__(self):
        self.turn = ''
        self.board = None

    def init(self, board: Board, turn: str):
        self.turn = turn
        self.board = board

    @abstractmethod
    def make_move(self):
        pass
