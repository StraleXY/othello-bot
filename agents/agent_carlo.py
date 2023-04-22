from agents.agent import Agent
from board import Board, BLACK, WHITE, MOVE, ROWS, COLS
import copy
import random
import math


class Node:

    def __init__(self, board: Board, turn: str, exploration: float, parent=None):
        self.exploration = exploration
        self.board = board
        self.turn = turn
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.board.find_all_legal_moves(self.turn))

    def is_terminal(self):
        return self.board.is_game_over()

    def expand(self):
        legal_moves = self.board.find_all_legal_moves(self.turn)
        for move in legal_moves:
            new_board = copy.deepcopy(self.board)
            new_board.move(*move, self.turn)
            new_node = Node(new_board, new_board.opposite_turn(self.turn), self.exploration, self)
            self.children.append(new_node)

    def select_child(self):
        if not self.children:
            return self
        best_child = None
        best_score = float("-inf")
        for child in self.children:
            if child.visits == 0:
                return child
            exploitation = child.wins / child.visits
            exploration = self.exploration * math.sqrt(math.log(self.visits) / child.visits)
            uct_score = exploitation + exploration
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    def back_propagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None:
            self.parent.back_propagate(result)


class CarloAgent(Agent):

    def __init__(self, num_simulations=1000, exploration=1.5):
        super().__init__()
        self.num_simulations = num_simulations
        self.exploration = exploration

    def make_move(self):
        root = Node(self.board, self.turn, self.exploration)

        for i in range(self.num_simulations):
            node = root
            board = copy.deepcopy(self.board)
            turn = self.turn
            while not node.is_terminal():
                if not node.is_fully_expanded():
                    node.expand()
                    node = node.select_child()
                    break
                else:
                    node = node.select_child()
                    next_moves = board.find_all_legal_moves(turn)
                    if not next_moves:
                        break
                    board.move(*random.choice(next_moves), turn)
                    turn = board.opposite_turn(turn)
            node.back_propagate(self.__simulate(board, turn))

        best_move = None
        best_visits = float("-inf")
        for child in root.children:
            if child.visits > best_visits:
                best_visits = child.visits
                best_move = child.board.last_move
        return best_move

    def __simulate(self, board, turn) -> int:
        while not board.is_game_over():
            moves = board.find_all_legal_moves(turn)
            if len(moves) == 0:
                turn = board.opposite_turn(turn)
                continue
            move = random.choice(moves)
            board.move(*move, turn)
            turn = board.opposite_turn(turn)
        result = board.return_winner()
        return 1 if result == self.turn else 0.5 if result is None else 0

