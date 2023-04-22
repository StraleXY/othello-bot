from agents.agent import Agent
from board import Board
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
            return self.__heuristic(board, turn)

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

