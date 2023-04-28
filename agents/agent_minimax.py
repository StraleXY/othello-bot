from agents.agent import Agent
from board import Board
from agents.utils import heuristic
import copy

class MinimaxAgent(Agent):

    def __init__(self, depth):
        super().__init__()
        self.depth = depth

    def make_move(self) -> (int, int):
        move = self.__search(self.board, self.turn, self.depth)
        # print(move)
        return move

    def __search(self, board, turn, depth):
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        moves = board.find_all_legal_moves(turn)

        if len(moves) == 0:
            print("FATAL ERROR")
            return None

        if len(moves) == 1:
            return moves[0]

        print("Calculating... {}".format(self.turn))
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.move(*move, self.turn)
            score = self.alpha_beta(new_board, self.board.opposite_turn(self.turn), depth, alpha, beta, False)
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)

        if best_move is None:
            return moves[0]

        return best_move

    def alpha_beta(self, board, turn, depth, alpha, beta, maximizing_turn):
        if depth == 0 or board.is_game_over():
            return heuristic(board, turn)

        if maximizing_turn:
            best_score = float('-inf')
            for move in board.find_all_legal_moves(turn):
                new_board = copy.deepcopy(board)
                new_board.move(*move, turn)
                score = self.alpha_beta(new_board, board.opposite_turn(turn), depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in board.find_all_legal_moves(turn):
                new_board = copy.deepcopy(board)
                new_board.move(*move, turn)
                score = self.alpha_beta(new_board, board.opposite_turn(turn), depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score