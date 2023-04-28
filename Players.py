import numpy as np

rng = np.random.default_rng()


class MCTSPlayer:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    # Simulates a random playout from the current game board until the game ends
    def simulate(self, board, player):
        # Continue simulating moves while the game is ongoing
        # still_turn = False
        cur_player = player
        while self.game.check_win(board) == 0:
            # Get a list of valid moves
            valid_moves = self.game.get_valid_moves(board, cur_player)
            # Select a random move from the list of valid moves
            valid_moves = np.nonzero(valid_moves)[0]
            random_idx = np.random.randint(len(valid_moves))
            random_move = valid_moves[random_idx]
            # while valid_moves[random_move] != 1:
            #     random_move = np.random.randint(self.game.get_action_size())
            # if len(valid_moves) == 0:
            #     break
            board, still_turn = self.game.place_move_n(board, cur_player, random_move)
            # Place the move on the board without checking for a win
            # Switch to the other player
            if not still_turn:
                cur_player = -cur_player
        # Return the game result
        return self.game.check_win(board)

    # Monte Carlo Tree Search function
    def play(self, board):
        # Initialize the best move and best score
        best_move = None
        best_score = float('-inf')
        player = 1
        new_board = np.copy(board)
        # Get a list of valid moves
        valid_moves = np.nonzero(self.game.get_valid_moves(new_board, 1))[0]
        # # If there's only one valid move, return it immediately
        if len(valid_moves) == 1:
            return valid_moves[0]

        # Loop through all valid moves
        for move in valid_moves:
            # Place the move on a copy of the board without checking for a win
            new_board, still_turn = self.game.place_move_n(new_board, player, move)
            # Initialize the number of wins for this move
            wins = 0

            # Perform a specified number of simulations for this move
            for _ in range(self.depth):
                # Simulate a random playout and get the game result
                simulation_result = self.simulate(new_board, player)
                # If the result is a win for the current player, increment the wins counter
                if simulation_result == 1:
                    wins += 1

            # Calculate the win rate for this move
            win_rate = wins / self.depth

            # If the win rate is higher than the current best score, update the best move and best score
            if win_rate > best_score:
                best_score = win_rate
                best_move = move

        # Return the best move found
        return best_move


class MinimaxPlayer:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    # MiniMax algorithm.
    def minimax(self, board, depth, player, isMaximizingPlayer, alpha, beta):
        win_check = self.game.check_win(board)
        if depth == 0 or (win_check == 1 or win_check == 2):
            return self.game.evaluate(player, board)

        if isMaximizingPlayer:
            best_value = float('-inf')
            for move in self.game.get_valid_moves(board, player).nonzero()[0]:
                new_board, still_turn = self.game.place_move_n(board, player, move)
                if still_turn:
                    value = self.minimax(new_board, depth - 1, player, True, alpha, beta)
                else:
                    value = self.minimax(new_board, depth - 1, -player, False, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = float('inf')
            for move in self.game.get_valid_moves(board, player).nonzero()[0]:
                new_board, still_turn = self.game.place_move_n(board, player, move)
                if still_turn:
                    value = self.minimax(new_board, depth - 1, player, True, alpha, beta)
                else:
                    value = self.minimax(new_board, depth - 1, -player, False, alpha, beta)
                best_value = min(best_value, value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    # Selects the best move from the list of available valid moves using the MiniMax algorithm.
    def play(self, board):
        game_board = np.copy(board)
        best_move = None
        best_value = float('-inf')
        player = 1
        valid_moves = self.game.get_valid_moves(game_board, player).nonzero()[0]

        if len(valid_moves) == 1:
            return valid_moves[0]

        for move in valid_moves:
            new_board, still_turn = self.game.place_move_n(board, player, move)
            if still_turn:
                value = self.game.evaluate(player, board)
                value += self.minimax(new_board, self.depth - 1, player, True, float('-inf'), float('inf'))
            else:
                value = self.minimax(new_board, self.depth - 1, -player, False, float('-inf'), float('inf'))
            if value >= best_value:
                best_value = value
                best_move = move

        return best_move


class HumanPlayer:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth

    def play(self, board):
        if board[4][-1]:
            return self.game.getActionSize() - 1
        valid_moves = self.game.get_valid_moves(board, 1)
        move = 0
        not_invalid = 1
        while not_invalid:
            print("Valid moves: {}".format(np.where(valid_moves == True)[0]))
            move = int(input())
            if valid_moves[move]:
                not_invalid = 0
            else:
                print("Invalid Move")
        return move
