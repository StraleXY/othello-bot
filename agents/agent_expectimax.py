import copy
from typing import Tuple
from agents.utils import heuristic
from math import inf
from agents.agent import Agent
from board import Board


class ExpectimaxAgent(Agent):
    def __init__(self, depth: int = 3):
        super().__init__()
        self.depth = depth

    def make_move(self):
        return self.__expectimax(self.board, self.turn, self.depth, True)[0]

    def __expectimax(self, board: Board, turn: str, depth: int, maximizing: bool):
        if depth == 0:
            return None, heuristic(board, turn)
        if board.is_game_over():
            return None, heuristic(board, turn)

        if maximizing:
            best_move = None
            best_score = -inf
            for move in board.find_all_legal_moves(turn):
                new_board = copy.deepcopy(board)
                new_board.move(move[0], move[1], turn)
                _, score = self.__expectimax(new_board, turn, depth - 1, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move, best_score

        else:
            total_score = 0
            num_moves = 0
            for move in board.find_all_legal_moves(turn):
                new_board = copy.deepcopy(board)
                new_board.move(move[0], move[1], turn)
                _, score = self.__expectimax(new_board, board.opposite_turn(turn), depth - 1, True)
                total_score += score
                num_moves += 1
            avg_score = total_score / num_moves
            return None, avg_score
