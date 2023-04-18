from agents.agent import Agent
import copy

class MinimaxAgent(Agent):

    def make_move(self) -> (int, int):
        move = self.__search(self.board, self.turn, 3)
        print(move)
        return move

    def __search(self, board, player, depth):
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in board.find_all_legal_moves(player):
            new_board = copy.deepcopy(board)
            new_board.move(*move)
            score = self.min_value(new_board, player, depth - 1, alpha, beta)
            if score > best_score:
                best_move = move
                best_score = score
            alpha = max(alpha, best_score)

        return best_move

    def max_value(self, board, player, depth, alpha, beta):
        """Get the maximum score for the current board state."""
        if depth == 0 or board.is_game_over():
            return self.__heuristic(board, player)

        best_score = float('-inf')

        for move in board.find_all_legal_moves(player):
            new_board = copy.deepcopy(board)
            new_board.move(*move)
            score = self.min_value(new_board, player, depth - 1, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score

    def min_value(self, board, player, depth, alpha, beta):
        """Get the minimum score for the current board state."""
        opponent = board.turn #BLACK if player == WHITE else WHITE

        if depth == 0 or board.is_game_over():
            return self.__heuristic(board, player)

        best_score = float('inf')

        for move in board.find_all_legal_moves(player):
            new_board = copy.deepcopy(board)
            new_board.move(*move)
            score = self.max_value(new_board, player, depth - 1, alpha, beta)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score

    def __heuristic(self, board, turn) -> float:
        return 1