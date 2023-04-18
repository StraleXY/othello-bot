EMPTY = '.'
WHITE = 'W'
BLACK = 'B'
MOVE = 'x'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class IllegalMoveException(Exception):
    pass


class Game:

    def __init__(self, turn: str, rows: int = 8, cols: int = 8):
        self.rows = rows
        self.cols = cols
        self.turn = turn  # Indicates who should play next 'B' or 'W'
        self.board = self.__new_board(rows, cols)

        legal_moves = self.find_all_legal_moves(self.turn)
        if legal_moves:
            self.__place_sequences(legal_moves, MOVE)
            self.print_board()

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_board(self):
        return self.board

    def get_turn(self):
        return self.turn

    def move(self, row: int, col: int) -> bool:
        sequences = self.__try_move(row, col, self.turn)
        if not sequences:
            return False
        self.__play_sequence(sequences)
        self.remove_pieces(MOVE)
        self.turn = self.opposite_turn(self.turn)
        # legal_moves = self.find_all_legal_moves(self.opposite_turn(self.turn))
        # if legal_moves:
        #     self.__place_sequences(legal_moves, MOVE)
        #     self.turn = self.opposite_turn(self.turn)
        return True

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
        for row in range(self.rows):
            for col in range(self.cols):
                if self.__is_legal_move(row, col, turn):
                    return True
        return False

    def find_all_legal_moves(self, turn) -> [(int, int)]:
        print("Looking for move {}".format(turn))
        self.print_board()
        legal_moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.__is_legal_move(row, col, turn):
                    legal_moves.append((row, col))
        return legal_moves

    def __is_legal_move(self, row, col, turn) -> bool:
        if self.board[row][col] != EMPTY and self.board[row][col] != MOVE:
            return False

        for row_direction, col_direction in DIRECTIONS:
            r, c = row + row_direction, col + col_direction
            taken_pieces = []
            while 0 <= r < self.rows and 0 <= c < self.cols:
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

    def __play_sequence(self, sequences: [[(int, int)]]):
        for sequence in sequences:
            self.__place_sequences(sequence, self.turn)

    def __place_sequences(self, sequence: [(int, int)], piece: str):
        for cell in sequence:
            self.board[cell[0]][cell[1]] = piece

    def remove_pieces(self, piece: str):
        self.board = [[EMPTY if element == piece else element for element in inner_lst] for inner_lst in self.board]

    @staticmethod
    def opposite_turn(turn: str):
        return WHITE if turn == BLACK else BLACK
