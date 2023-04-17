EMPTY = '.'
WHITE = 'W'
BLACK = 'B'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class IllegalMoveException(Exception):
    pass


class Game:

    def __init__(self, turn: str, rows: int = 8, cols: int = 8):
        self.rows = rows
        self.cols = cols
        self.turn = turn  # Indicates who should play next 'B' or 'W'
        self.board = self.__new_board(rows, cols)

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_board(self):
        return self.board

    def get_turn(self):
        return self.turn

    def move(self, row: int, col: int) -> bool:
        sequences = self.is_valid_move(row, col, self.turn)
        if not sequences:
            return False
        self.__play_sequences(sequences)
        if self.has_legal_moves(self.turn):
            self.turn = self.opposite_turn(self.turn)
        return True

    def is_game_over(self) -> bool:
        return not self.has_legal_moves(BLACK) and not self.has_legal_moves(WHITE)

    def return_winner(self) -> str:
        black_score = self.__get_cells_count(BLACK)
        white_score = self.__get_cells_count(WHITE)
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

    def __get_cells_count(self, turn: str) -> int:
        return sum(1 for row in self.board for cell in row if cell == turn)

    # TODO Make private
    def has_legal_moves(self, turn) -> bool:
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == EMPTY:
                    if self.is_valid_move(row, col, self.opposite_turn(turn)):
                        return True
        return False

    # TODO Make private
    def is_valid_move(self, row, col, turn) -> [[(int, int)]]:
        if self.board[row][col] != EMPTY:
            return False

        valid_sequences = []

        for row_direction, col_direction in DIRECTIONS:
            r, c = row + row_direction, col + col_direction
            taken_pieces = []
            sequence = [(row, col)]
            while 0 <= r < self.rows and 0 <= c < self.cols:
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

    def __play_sequences(self, sequences: [[(int, int)]]):
        for sequence in sequences:
            for cell in sequence:
                self.board[cell[0]][cell[1]] = self.turn

    @staticmethod
    def opposite_turn(turn: str):
        return WHITE if turn == BLACK else BLACK
