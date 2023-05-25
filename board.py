EMPTY = '.'
WHITE = 'W'
BLACK = 'B'
ROWS = 8
COLS = 8
MOVE = 'x'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Board:

    def __init__(self, turn: str):
        self.board = self.__new_board(ROWS, COLS)
        self.last_move = None

        legal_moves = self.find_all_legal_moves(turn)
        if legal_moves:
            self.__place_sequences(legal_moves, MOVE)

    def get_board(self):
        return self.board

    def find_all_legal_moves(self, turn) -> [(int, int)]:
        legal_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.__is_legal_move(row, col, turn):
                    legal_moves.append((row, col))
        return legal_moves

    def move(self, row: int, col: int, turn: str) -> (bool, str):
        sequences = self.__try_move(row, col, turn)
        if not sequences:
            return False, turn
        self.__play_sequence(sequences, turn)
        self.remove_pieces(MOVE)
        self.last_move = (row, col)
        if self.__prepare_moves(self.opposite_turn(turn)):
            return True, self.opposite_turn(turn)
        else:
            self.__prepare_moves(turn)
            return True, turn

    def get_corners(self, turn):
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        num_corners = 0
        for corner in corners:
            if self.board[corner[0]][corner[1]] == turn:
                num_corners += 1
        return num_corners

    def get_cells_count(self, turn: str) -> int:
        return sum(1 for row in self.board for cell in row if cell == turn)

    def is_game_over(self) -> bool:
        return not self.__has_legal_moves(BLACK) and not self.__has_legal_moves(WHITE)

    def return_winner(self) -> str:
        black_score = self.get_cells_count(BLACK)
        white_score = self.get_cells_count(WHITE)
        return WHITE if white_score > black_score else BLACK if black_score > white_score else None

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print('---------------')

    # Private
    @staticmethod
    def __new_board(rows: int, cols: int) -> [[str]]:
        _board = [[EMPTY for _ in range(cols)] for _ in range(rows)]
        _board[rows // 2 - 1][cols // 2 - 1] = WHITE
        _board[rows // 2 - 1][cols // 2] = BLACK
        _board[rows // 2][cols // 2 - 1] = BLACK
        _board[rows // 2][cols // 2] = WHITE
        return _board

    def __has_legal_moves(self, turn) -> bool:
        for row in range(ROWS):
            for col in range(COLS):
                if self.__is_legal_move(row, col, turn):
                    return True
        return False

    def __is_legal_move(self, row, col, turn) -> bool:
        if self.board[row][col] != EMPTY and self.board[row][col] != MOVE:
            return False

        for row_direction, col_direction in DIRECTIONS:
            r, c = row + row_direction, col + col_direction
            taken_pieces = []
            while 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == EMPTY:
                    break
                elif self.board[r][c] == turn:
                    if taken_pieces:
                        return True
                    else:
                        break
                if self.board[r][c] == MOVE:
                    break
                else:
                    taken_pieces.append(self.board[r][c])
                    r += row_direction
                    c += col_direction

        return False

    def __try_move(self, row, col, turn) -> [[(int, int)]]:
        if self.board[row][col] != MOVE:
            return False

        valid_sequences = []

        for row_direction, col_direction in DIRECTIONS:
            r, c = row + row_direction, col + col_direction
            taken_pieces = []
            sequence = [(row, col)]
            while 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == self.opposite_turn(turn):
                    taken_pieces.append(self.board[r][c])
                    sequence.append((r, c))
                    r += row_direction
                    c += col_direction
                elif self.board[r][c] == turn and taken_pieces:
                    sequence.append((r, c))
                    valid_sequences.append(sequence)
                    break
                else:
                    break

        return valid_sequences

    def __prepare_moves(self, turn) -> bool:
        legal_moves = self.find_all_legal_moves(turn)
        if legal_moves:
            self.__place_sequences(legal_moves, MOVE)
            return True
        return False

    def __play_sequence(self, sequences: [[(int, int)]], turn: str):
        for sequence in sequences:
            self.__place_sequences(sequence, turn)

    def __place_sequences(self, sequence: [(int, int)], turn: str):
        for cell in sequence:
            self.board[cell[0]][cell[1]] = turn

    def remove_pieces(self, turn: str):
        self.board = [[EMPTY if element == turn else element for element in inner_lst] for inner_lst in self.board]

    @staticmethod
    def opposite_turn(turn: str):
        return WHITE if turn == BLACK else BLACK
