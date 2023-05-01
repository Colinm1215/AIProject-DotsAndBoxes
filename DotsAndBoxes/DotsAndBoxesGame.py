import numpy as np


class DotsAndBoxesGame:
    def __init__(self, n):
        self.n = n
        self.completed_boxes = [[]]
        self.board_size = 2 * self.n + 1, self.n + 1
        self.action_size = 2 * (self.n + 1) * self.n + 1

    @staticmethod
    def read_gamestate(file_path):
        board = np.loadtxt(file_path, dtype=int)
        return board

    # Creates a new gamestate of a size selected by the user. Used if no scenario is given.
    def create_gameboard(self, size):
        self.completed_boxes = np.zeros([self.n, self.n], dtype=int)
        board = np.zeros((size * 2 + 1, size + 1), dtype=int)
        return board

    def create_board(self, size):
        self.completed_boxes = np.zeros([self.n, self.n], dtype=int)
        board = np.zeros((size * 2 + 1, size + 1), dtype=int)
        return board

    @staticmethod
    def is_still_turn(board):
        return board[4][-1]

    @staticmethod
    def toggle_turn(board, turn=False):
        board[4][-1] = turn

    @staticmethod
    def get_canonical_form(board, player):
        board = np.copy(board)
        if player == -1:
            # swap score
            aux = board[0, -1]
            board[0, -1] = board[2, -1]
            board[2, -1] = aux
        return board

    def display_board(self, board):
        n = board.shape[1]
        for i in range(n):
            print("")
            for j in range(n - 1):
                s = "o x " if board[i][j] else "o   "
                print(s, end="")
            print("o")
            if i < n - 1:
                for j in range(n):
                    s = "x " if board[i + n][j] else "| "
                    if j < n - 1:
                        a = self.completed_boxes[i][j]
                        if a != 0:
                           s += " X "
                    print(s, end="")
        print("Pass: {}".format(board[4, -1]))
        print("Score {} x {}".format(board[0, -1], board[2, -1]))

    @staticmethod
    def stringRepresentation(board):
        return board.tobytes()

    def check_score(self, board, move_r, move_c, player, get_boxes=False):
        b = board
        b1 = 0
        b2 = 0
        # if horizontal
        if move_r % 2 == 0:
            # find box below
            if move_r < 2 * self.n:
                b1 = b[move_r + 1][move_c] and b[move_r + 2][move_c] and b[move_r + 1][move_c + 1]
                if b1 and get_boxes:
                    self.completed_boxes[move_r // 2][move_c] = player
            # find box above
            if move_r > 0:
                b2 = b[move_r - 2][move_c] and b[move_r - 1][move_c] and b[move_r - 1][move_c + 1]
                if b2 and get_boxes:
                    self.completed_boxes[(move_r - 2) // 2][move_c] = player
        # is vertical
        elif move_r % 2 != 0:
            if move_c < len(b[move_r]) - 1:
                b1 = b[move_r][move_c + 1] and b[move_r + 1][move_c] and b[move_r - 1][move_c]
                if b1 and get_boxes:
                    self.completed_boxes[(move_r - 1) // 2][move_c] = player
            if move_c > 0:
                b2 = b[move_r][move_c - 1] and b[move_r - 1][move_c - 1] and b[move_r + 1][move_c - 1]
                if b2 and get_boxes:
                    self.completed_boxes[(move_r - 1) // 2][move_c - 1] = player
        still_turn = b1 or b2
        if still_turn:
            if player == 1:
                board[0][-1] += b1 + b2
            else:
                board[2][-1] += b1 + b2
        return still_turn

    def get_next_state(self, board, player, action, get_boxes=False):
        b = np.copy(board)
        if action == self.action_size - 1:
            b[4, -1] = 0
        else:
            b, still_turn = self.place_move(b, player, action, get_boxes)
            b[4, -1] = still_turn
        return b, -player

    def place_move(self, board, player, action, get_boxes=False):
        if action == self.action_size - 1:
            board[4][-1] = 0
            return board, False
        is_horizontal = action < self.n * (self.n + 1)
        if is_horizontal:
            move = ((action // self.n) * 2, action % self.n)
        else:
            action -= self.n * (self.n + 1)
            move = ((action // (self.n + 1)) * 2 + 1, action % (self.n + 1))
        (move_r, move_c) = move
        board[move_r][move_c] = 1
        still_turn = self.check_score(board, move_r, move_c, player, get_boxes)
        return board, still_turn

    # Checks if the game is finished and if so, who the winner is.
    # Returns 0 if board not finished.
    # Returns 1 if player 1 wins.
    # Returns 2 if player 2 wins.
    # Returns 3 if a tie occurs.
    def check_win(self, board):
        player1_count = board[0][-1]
        player2_count = board[2][-1]
        if self.has_valid_moves(board):
            return 0
        else:
            if player1_count > player2_count:
                return 1
            elif player2_count > player1_count:
                return 2
            else:
                return 3

    def get_game_ended(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        if self.has_valid_moves(board):
            return 0

        if board[0][-1] == board[2][-1]:
            return 2
        else:
            player_1_won = board[0][-1] > board[2][-1]
            return 1 * player if player_1_won else -1 * player

    # Evaluates the current score of the game.
    @staticmethod
    def evaluate(player, board):
        player1_count = board[0][-1]
        player2_count = board[2][-1]

        if player == 1:
            return player1_count - player2_count
        else:
            return player2_count - player1_count

    # Returns all remaining valid moves available to a player.
    def get_valid_moves_coords(self, board):
        valid_moves = np.transpose(np.nonzero(board == 0))
        valid_moves = np.delete(valid_moves, np.where((valid_moves[:, 0] % 2 == 0) & (valid_moves[:, 1] == self.n))[0],
                                axis=0)
        return valid_moves

    def get_valid_moves(self, board, player):
        valid_moves = np.logical_not(board)
        valid_moves = np.hstack((valid_moves[:self.board_size[0]:2, :-1].flatten(),
                                 valid_moves[1:self.board_size[0]:2, :].flatten(), False))
        if board[4, -1]:
            valid_moves[:] = False
            valid_moves[-1] = True
        return valid_moves

    def has_valid_moves(self, board):
        is_board_full = np.all(board[:self.board_size[0]:2, :-1]) and np.all(board[1:self.board_size[0]:2, :])
        return not is_board_full

    def in_valid_moves(self, move_r, move_c, game_board):
        valid_moves = self.get_valid_moves_coords(game_board)
        valid = False
        for move in valid_moves:
            if move_r == move[0] and move_c == move[1]:
                valid = True
        return valid

    @staticmethod
    def dispDummy(board):
        pass

    def getSymmetries(self, board, pi):
        # mirror, rotational

        horizontal = np.copy(board[:self.board_size[0]:2, :-1])
        vertical = np.copy(board[1:self.board_size[0]:2, :])
        t = self.n * (self.n + 1)
        pi_horizontal = np.copy(pi[:t]).reshape((self.n + 1, self.n))
        pi_vertical = np.copy(pi[t:-1]).reshape((self.n, self.n + 1))

        l = []

        for i in range(1, 5):
            horizontal = np.rot90(horizontal)
            vertical = np.rot90(vertical)
            pi_horizontal = np.rot90(pi_horizontal)
            pi_vertical = np.rot90(pi_vertical)

            for _ in [True, False]:
                horizontal = np.fliplr(horizontal)
                vertical = np.fliplr(vertical)
                pi_horizontal = np.fliplr(pi_horizontal)
                pi_vertical = np.fliplr(pi_vertical)

                new_board = self.create_board(self.n)
                new_board[:self.board_size[0]:2, :-1] = vertical
                new_board[1:self.board_size[0]:2, :] = horizontal

                l += [(new_board, list(pi_vertical.ravel()) + list(pi_horizontal.ravel()) + [pi[-1]])]

            aux = horizontal
            horizontal = vertical
            vertical = aux

            aux = pi_horizontal
            pi_horizontal = pi_vertical
            pi_vertical = aux
        return l
