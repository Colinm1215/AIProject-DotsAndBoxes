import random
import numpy as np


class DotsAndBoxes:
    def __init__(self, n):
        self.n = n
        self.completed_boxes = [[]]
        self.board_size = 2 * self.n + 1, self.n + 1
        self.action_size = 2 * (self.n + 1) * self.n + 1

    # Reads in a given scenario game state.
    def read_gamestate(self, file_path):
        f = open(file_path, "r")
        first_row = f.readline()
        board = self.create_gameboard(len(first_row) - 2)
        f = open(file_path, "r")
        row = 0
        col = 0
        for x in f:
            if x == "\n" or x == "":
                continue
            x = x.strip("\n")
            for c in x:
                if row % 2 == 0:
                    if row == len(board):
                        continue
                    if col == len(board[0]):
                        continue
                if c == "\n":
                    continue
                if c == "1":
                    board[row][col] = 1
                else:
                    board[row][col] = 0
                col += 1
                # Shouldn't be needed
                # print_board(board)
            col = 0
            row += 1

        return board

    # Creates a new gamestate of a size selected by the user. Used if no scenario is given.
    def create_gameboard(self, size):
        self.completed_boxes = np.zeros([3, 3], dtype=int)
        board = np.zeros((size * 2 + 1, size + 1), dtype=int)
        return board

    def create_board(self, size):
        self.completed_boxes = np.zeros([3, 3], dtype=int)
        board = np.zeros((size * 2 + 1, size + 1), dtype=int)
        return board

    def get_action_size(self):
        return self.action_size

    @staticmethod
    def is_still_turn(board):
        return board[4][-1]

    @staticmethod
    def get_canonical_form(board, player):
        board = np.copy(board)
        if player == 2:
            # swap score
            aux = board[0, -1]
            board[0, -1] = board[2, -1]
            board[2, -1] = aux
        return board

    # Prints the game board.
    def print_board(self, board):
        o_size = len(board[0])
        for row in range(len(board)):
            if len(board[row]) == len(board[0]):
                type = "row"
                stri = "O"
            else:
                type = "col"
                stri = ""
            for col in range(len(board[row])):
                if board[row][col] == 1:
                    if type == "row":
                        stri += "-O"
                    else:
                        if col <= len(board[row]) - 2:
                            if self.completed_boxes[(row - 1) // 2][col] == 0:
                                stri += "| "
                            else:
                                stri += "|" + str(self.completed_boxes[(row - 1) // 2][col])
                        else:
                            stri += "|"
                else:
                    if type == "row":
                        stri += " O"
                    else:
                        stri += "  "
            print(stri)
        print()

    @staticmethod
    def display_board(board):
        n = board.shape[1]
        for i in range(n):
            for j in range(n - 1):
                s = "*-x-" if board[i][j] else "*---"
                print(s, end="")
            print("*")
            if i < n - 1:
                for j in range(n):
                    s = "x   " if board[i + n][j] else "|   "
                    print(s, end="")
            print("")

    @staticmethod
    def stringRepresentation(board):
        return board.tostring()

    def check_completed_box(self, board, move_r, move_c, player, pri, completed_boxes_t=None):
        # print(f'row:{move_r}, col:{move_c}')
        if completed_boxes_t is None:
            completed_boxes_temp = np.copy(self.completed_boxes)
        else:
            completed_boxes_temp = completed_boxes_t
        b = board
        still_turn = False
        b1 = 0
        b2 = 0
        # if horizontal
        if move_r % 2 == 0:
            # find box below
            if move_r < 2 * self.n:
                b1 = b[move_r + 1][move_c] and b[move_r + 2][move_c] and b[move_r + 1][move_c + 1]
            # find box above
            if move_r > 0:
                b2 = b[move_r - 2][move_c] and b[move_r - 1][move_c] and b[move_r - 1][move_c + 1]

            if b1:
                completed_boxes_temp[move_r // 2][move_c] = player
            if b2:
                completed_boxes_temp[(move_r - 2) // 2][move_c] = player
            # print(f'Box1: {b1} Box2: {b2}')
        # is vertical
        elif move_r % 2 != 0:
            if move_c < len(b[move_r]) - 1:
                b1 = b[move_r][move_c + 1] and b[move_r + 1][move_c] and b[move_r - 1][move_c]
            if move_c > 0:
                b2 = b[move_r][move_c - 1] and b[move_r - 1][move_c - 1] and b[move_r + 1][move_c - 1]
            if b1:
                completed_boxes_temp[(move_r - 1) // 2][move_c] = player
            if b2:
                completed_boxes_temp[(move_r - 1) // 2][move_c - 1] = player
            # print(f'Box1: {b1} Box2: {b2}')
        still_turn = b1 or b2
        if still_turn:
            if player == 1:
                board[0][-1] += b1 + b2
            else:
                board[2][-1] += b1 + b2
        if pri:
            self.completed_boxes = completed_boxes_temp
            return still_turn, self.completed_boxes
        else:
            return still_turn, completed_boxes_temp

    def get_completed_boxes_old(self, board, move_r, move_c, player, pri):
        completed_boxes_temp = np.copy(self.completed_boxes)
        print(f'row:{move_r}, col:{move_c}')
        still_turn = False
        # Check if the current move is on a horizontal line
        if move_r % 2 == 0:
            # Check if there's a row above the current move
            if move_r > 0:
                # Check if there's a completed box above the current move
                if (
                        board[move_r - 1][move_c - 1]  # Line to the right and above the current move
                        and board[move_r - 1][move_c]  # Line above the current move
                        and board[move_r - 1][move_c + 1]  # Line to the left and above the current move
                ):
                    # Update the completed_boxes entry for the box above the current move
                    completed_boxes_temp[(move_r - 2) // 2][move_c] = player
                    still_turn = True
            # Check if there's a row below the current move
            if move_r < len(board) - 2:
                # Check if there's a completed box below the current move
                if (
                        board[move_r + 1][move_c + 1]  # Line to the right and below the current move
                        and board[move_r + 1][move_c]  # Line below the current move
                        and board[move_r + 2][move_c]  # Line to the left and below the current move
                ):
                    # Update the completed_boxes entry for the box below the current move
                    completed_boxes_temp[move_r // 2][move_c] = player
                    still_turn = True
        # Check if the current move is on a vertical line
        elif move_r % 2 != 0:
            # Check if there's a column to the left of the current move
            if move_c > 0:
                # Check if there's a completed box to the left of the current move
                if (
                        board[move_r][move_c - 1]  # Line to the left of the current move
                        and board[move_r - 1][move_c - 1]  # Line above and to the left of the current move
                        and board[move_r + 1][move_c - 1]  # Line below and to the left of the current move
                ):
                    # Update the completed_boxes entry for the box to the left of the current move
                    completed_boxes_temp[(move_r - 1) // 2][move_c - 1] = player
                    still_turn = True
            # Check if there's a column to the right of the current move
            if move_c <= len(board[move_r]) - 2:
                # Check if there's a completed box to the right of the current move
                if (
                        board[move_r][move_c + 1]  # Line to the right of the current move
                        and board[move_r - 1][move_c]  # Line above and to the right of the current move
                        and board[move_r + 1][move_c]  # Line below and to the right of the current move
                ):
                    # Update the completed_boxes entry for the box to the right of the current move
                    completed_boxes_temp[(move_r - 1) // 2][move_c] = player
                    still_turn = True

        if pri:
            self.completed_boxes = completed_boxes_temp
        return still_turn

    def getNextState(self, board, player, action):
        b = np.copy(board)
        if action == self.action_size - 1:
            board[4, -1] = 0
        else:
            self.place_move()

        return board, -player

    def has_legal_moves(self, board):
        is_board_full = np.all(board[:self.n + 1, :-1]) and np.all(board[-self.n:, :])
        return not is_board_full

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        if self.has_legal_moves:
            return 0

        if board[0][-1] == board[2][-1]:
            return -1 * player
        else:
            player_1_won = board[0][-1] > board[2][-1]
            return 1 * player if player_1_won else -1 * player

    # def getSymmetries(self, board, pi):
    #     # mirror, rotational
    #
    #     horizontal = np.copy(board[:self.n + 1, :self.n])
    #     vertical = np.copy(board[-self.n:, :])
    #     t = self.n * (self.n + 1)
    #     pi_horizontal = np.copy(pi[:t]).reshape((self.n + 1, self.n))
    #     pi_vertical = np.copy(pi[t:-1]).reshape((self.n, self.n + 1))
    #
    #     l = []
    #
    #     for i in range(1, 5):
    #         horizontal = np.rot90(horizontal)
    #         vertical = np.rot90(vertical)
    #         pi_horizontal = np.rot90(pi_horizontal)
    #         pi_vertical = np.rot90(pi_vertical)
    #
    #         for _ in [True, False]:
    #             horizontal = np.fliplr(horizontal)
    #             vertical = np.fliplr(vertical)
    #             pi_horizontal = np.fliplr(pi_horizontal)
    #             pi_vertical = np.fliplr(pi_vertical)
    #
    #             new_board = Board(self.n)
    #             new_board.pieces = np.copy(board)
    #             new_board.pieces[:self.n + 1, :self.n] = vertical
    #             new_board.pieces[-self.n:, :] = horizontal
    #
    #             l += [(new_board.pieces, list(pi_vertical.ravel()) + list(pi_horizontal.ravel()) + [pi[-1]])]
    #
    #         aux = horizontal
    #         horizontal = vertical
    #         vertical = aux
    #
    #         aux = pi_horizontal
    #         pi_horizontal = pi_vertical
    #         pi_vertical = aux
    #     return l

    # TODO_ Make actions boolean array
    def place_move_2(self, board, player, action, print, completed_boxes_t):
        is_horizontal = action < self.n * (self.n + 1)
        if is_horizontal:
            move = (int(action / self.n), action % self.n)
        else:
            action -= self.n * (self.n + 1)
            move = (int(action / (self.n + 1)) + self.n + 1, action % (self.n + 1))
        (move_r, move_c) = move
        still_turn, completed_boxes = self.check_completed_box(board, move_r, move_c, player, print, completed_boxes_t)
        return board, still_turn, completed_boxes

    # Checks if moves are valid and how they should be made (horizontal or vertical). Adds player # to completed boxes.
    def place_move(self, board, player, move_r, move_c, print, completed_boxes_t=None):
        board[move_r][move_c] = 1
        still_turn, completed_boxes = self.check_completed_box(board, move_r, move_c, player, print, completed_boxes_t)
        return board, still_turn, completed_boxes

    # Checks if the game is finished and if so, who the winner is.
    # Returns 0 if board not finished.
    # Returns 1 if player 1 wins.
    # Returns 2 if player 2 wins.
    # Returns 3 if a tie occurs.
    def check_win(self, board):
        player1_count = board[0][-1]
        player2_count = board[2][-1]
        size = self.n
        if player2_count + player1_count != size * size:
            return 0
        else:
            if player1_count > player2_count:
                return 1
            elif player2_count > player1_count:
                return 2
            else:
                return 3

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
    def get_valid_moves_old(self, board):
        valid_moves = []
        leng = 0
        for r in range(2 * self.n + 1):
            if r % 2 == 0:
                leng = len(board[r]) - 1
            else:
                leng = len(board[r])
            for c in range(leng):
                if board[r][c] == 0:
                    valid_moves.append([r, c])
        # print(valid_moves)
        return valid_moves

    def get_valid_moves(self, board):
        valid_moves = np.transpose(np.nonzero(board == 0))
        valid_moves = np.delete(valid_moves, np.where((valid_moves[:, 0] % 2 == 0) & (valid_moves[:, 1] == self.n))[0],
                                axis=0)
        return valid_moves

    def getValidMoves(self, board, player):
        legal_moves = np.logical_not(board)
        legal_moves = np.hstack((legal_moves[:self.board_size[0]:2, :-1].flatten(), legal_moves[1:self.board_size[0]:2, :].flatten(), False))
        # legal_moves = np.hstack((legal_moves[:self.n + 1, :-1].flatten(), legal_moves[-self.n:, :].flatten(), False))
        return legal_moves

    # MiniMax algorithm.
    def minimax(self, board, depth, player, isMaximizingPlayer, alpha, beta, completed_boxes_temp):
        win_check = self.check_win(board)
        if depth == 0 or (win_check == 1 or win_check == 2):
            return self.evaluate(player, board)

        if isMaximizingPlayer:
            best_value = float('-inf')
            for move in self.get_valid_moves(board):
                new_board, still_turn, completed_boxes_temp = self.place_move(board, player, move[0], move[1], False)
                if still_turn:
                    value = self.minimax(new_board, depth - 1, player, True, alpha, beta, completed_boxes_temp)
                else:
                    next_player = 2 if player == 1 else 1
                    value = self.minimax(new_board, depth - 1, next_player, False, alpha, beta, completed_boxes_temp)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = float('inf')
            for move in self.get_valid_moves(board):
                new_board, still_turn, completed_boxes_temp = self.place_move(board, player, move[0], move[1], False)
                if still_turn:
                    value = self.minimax(new_board, depth - 1, player, False, alpha, beta, completed_boxes_temp)
                else:
                    next_player = 2 if player == 1 else 1
                    value = self.minimax(new_board, depth - 1, next_player, True, alpha, beta, completed_boxes_temp)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    # Selects the best move from the list of available valid moves using the MiniMax algorithm.
    def get_best_move_minimax(self, board, depth, player):
        game_board = np.copy(board)
        best_move = None
        best_value = float('-inf')

        move_list = self.get_valid_moves(game_board)

        if len(move_list) == 1:
            return move_list[0]

        for move in move_list:
            new_board, still_turn, completed_boxes_temp = self.place_move(game_board, player, move[0], move[1], False)
            if still_turn:
                value = self.evaluate(player, board)
                value += self.minimax(new_board, depth - 1, player, True, float('-inf'), float('inf'),
                                      completed_boxes_temp)
            else:
                next_player = 2 if player == 1 else 1
                value = self.minimax(new_board, depth - 1, next_player, False, float('-inf'), float('inf'),
                                     completed_boxes_temp)
            if value >= best_value:
                best_value = value
                best_move = move

        return best_move

    def in_valid_moves(self, move_r, move_c, game_board):
        valid_moves = self.get_valid_moves(game_board)
        valid = False
        for move in valid_moves:
            if move_r == move[0] and move_c == move[1]:
                valid = True
        return valid

    # Simulates a random playout from the current game board until the game ends
    def simulate(self, board, player, completed_boxes_temp):
        # Continue simulating moves while the game is ongoing
        while self.check_win(board) == 0:
            # Get a list of valid moves
            valid_moves = self.get_valid_moves(board)
            # Select a random move from the list of valid moves
            if len(valid_moves) > 0:
                random_move = random.choice(valid_moves)
            else:
                break
            # Extract row and column from the selected move
            move_r = random_move[0]
            move_c = random_move[1]
            # Place the move on the board without checking for a win
            board, still_turn, completed_boxes_temp = self.place_move(board, player, move_r, move_c, False,
                                                                      completed_boxes_temp)
            # Switch to the other player
            if not still_turn:
                if player == 1:
                    player = 2
                else:
                    player = 1
        # Return the game result (1, 2, or 3)
        return self.check_win(board)

    # Monte Carlo Tree Search function
    def mcts(self, board, player, num_simulations):
        # Initialize the best move and best score
        best_move = None
        best_score = float('-inf')

        # Get a list of valid moves
        valid_moves = self.get_valid_moves(board)

        # If there's only one valid move, return it immediately
        if len(valid_moves) == 1:
            return valid_moves[0]

        # Loop through all valid moves
        for move in valid_moves:
            # Extract row and column from the current move
            move_r, move_c = move
            # Place the move on a copy of the board without checking for a win
            new_board, still_turn, completed_boxes_temp = self.place_move(np.copy(board), player, move_r, move_c, False)
            # Initialize the number of wins for this move
            wins = 0

            # Perform a specified number of simulations for this move
            for _ in range(num_simulations):
                # Simulate a random playout and get the game result
                simulation_result = self.simulate(new_board, player, completed_boxes_temp)
                # If the result is a win for the current player, increment the wins counter
                if simulation_result == player:
                    wins += 1

            # Calculate the win rate for this move
            win_rate = wins / num_simulations

            # If the win rate is higher than the current best score, update the best move and best score
            if win_rate > best_score:
                best_score = win_rate
                best_move = move

        # Return the best move found
        return best_move

    def perform_turn_manual(self, board, player):
        player_move_row = int(input("Enter Move Row : "))
        player_move_col = int(input("Enter Move Col : "))
        while not self.in_valid_moves(player_move_row, player_move_col, board):
            print("Invalid Move")
            player_move_row = int(input("Enter Move Row : "))
            player_move_col = int(input("Enter Move Col : "))

        print("Placing at ", [player_move_row, player_move_col])
        return self.place_move(board, player, player_move_row, player_move_col, True)

    def perform_turn_minimax(self, board, player, depth):
        move = self.get_best_move_minimax(board, depth, player)
        print("Placing at ", move)
        return self.place_move(board, player, move[0], move[1], True)

    def perform_turn_mcts(self, board, player, depth):
        move = self.mcts(board, player, depth)
        # print("Placing at ", move)
        return self.place_move(board, player, move[0], move[1], True)

    def switch_for_turn_type(self, board, player, depth, type):
        if type == "minimax":
            return self.perform_turn_minimax(board, player, depth)
        elif type == "mcts":
            return self.perform_turn_mcts(board, player, depth)
        elif type == "manual":
            return self.perform_turn_manual(board, player)
        else:
            return None, False
