from agents.agent import Agent
from board import Board, BLACK, WHITE, MOVE, ROWS, COLS
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
            return self.__heuristic(board, turn)
        moves = board.find_all_legal_moves(turn)
        if not moves:
            return self.alpha_beta(board, depth - 1, alpha, beta, board.opposite_turn(turn), probcut)
        if depth == self.depth:
            move_scores = []
            for move in moves:
                new_board = copy.deepcopy(board)
                new_board.move(*move, turn)
                score = self.__heuristic(new_board, turn)
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

    def __heuristic(self, board: Board, turn):

        opponent = board.opposite_turn(turn)
        weights = [
            [4, -3, 2, 2, 2, 2, -3, 4],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 0, 1, 1, 0, -1, 2],
            [2, -1, 1, 0, 0, 1, -1, 2],
            [-3, -4, -1, -1, -1, -1, -4, -3],
            [4, -3, 2, 2, 2, 2, -3, 4],
        ]
        position_score = 0
        for i in range(8):
            for j in range(8):
                if board.board[i][j] == turn:
                    position_score += weights[i][j]
                elif board.board[i][j] == opponent:
                    position_score -= weights[i][j]

        turn_count = board.get_cells_count(turn)
        opponent_count = board.get_cells_count(opponent)
        disk_score = 100 * (turn_count - opponent_count) / (turn_count + opponent_count + 1)

        turn_moves = board.find_all_legal_moves(turn)
        opponent_moves = board.find_all_legal_moves(opponent)
        mobility_score = 100 * (len(turn_moves) - len(opponent_moves)) / (len(turn_moves) + len(opponent_moves) + 1)

        turn_corners_count = board.get_corners(turn)
        opponent_corners_count = board.get_corners(opponent)
        if turn_corners_count + opponent_corners_count != 0:
            corner_score = 100 * (turn_corners_count - opponent_corners_count) / (turn_corners_count + opponent_corners_count)
        else:
            corner_score = 0

        return (0.06 * mobility_score) + (0.6 * corner_score) + (0.25 * disk_score) + (0.09 * position_score)
