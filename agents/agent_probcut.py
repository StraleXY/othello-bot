from agents.agent import Agent
from board import Board, BLACK, WHITE, MOVE, ROWS, COLS
from agents.utils import heuristic
import copy
import random


class ProbCutAgent(Agent):

    def __init__(self, depth=3, probcut=0.1):
        super().__init__()
        self.depth = depth
        self.probcut = probcut

    def make_move(self):
        moves = self.board.find_all_legal_moves(self.turn)
        if not moves:
            return None
        if len(moves) == 1:
            return moves[0]
        best_move = None
        best_score = float("-inf")
        for move in moves:
            board = copy.deepcopy(self.board)
            board.move(*move, self.turn)
            score = self.alpha_beta(board, self.depth, float("-inf"), float("inf"), self.turn, self.probcut)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def alpha_beta(self, board, depth, alpha, beta, turn, probcut):
        if depth == 0 or board.is_game_over():
            return heuristic(board, turn)
        moves = board.find_all_legal_moves(turn)
        if not moves:
            return self.alpha_beta(board, depth - 1, alpha, beta, board.opposite_turn(turn), probcut)
        if depth == self.depth:
            move_scores = []
            for move in moves:
                new_board = copy.deepcopy(board)
                new_board.move(*move, turn)
                score = heuristic(new_board, turn)
                move_scores.append((move, score))
            move_scores.sort(key=lambda x: x[1], reverse=True)
            best_moves = [move_scores[0][0]]
            for move, score in move_scores[1:]:
                if score >= move_scores[0][1] - probcut:
                    best_moves.append(move)
                else:
                    break
            moves = best_moves
        if turn == self.turn:
            for move in moves:
                new_board = copy.deepcopy(board)
                new_board.move(*move, turn)
                alpha = max(alpha, self.alpha_beta(new_board, depth - 1, alpha, beta, new_board.opposite_turn(turn), probcut))
                if alpha >= beta:
                    break
            return alpha
        else:
            for move in moves:
                new_board = copy.deepcopy(board)
                new_board.move(*move, turn)
                beta = min(beta, self.alpha_beta(new_board, depth - 1, alpha, beta, new_board.opposite_turn(turn), probcut))
                if beta <= alpha:
                    break
            return beta