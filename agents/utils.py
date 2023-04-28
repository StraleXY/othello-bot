from board import Board, BLACK, WHITE, MOVE, ROWS, COLS

def heuristic(board: Board, turn):
    return __optimal_heuristic(board, turn)


def __optimal_heuristic(board: Board, turn):
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
        corner_score = 100 * (turn_corners_count - opponent_corners_count) / (
                    turn_corners_count + opponent_corners_count)
    else:
        corner_score = 0

    return (0.06 * mobility_score) + (0.6 * corner_score) + (0.25 * disk_score) + (0.09 * position_score)
