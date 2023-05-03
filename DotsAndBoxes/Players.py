import os
import numpy as np

from AlphaZero.keras.NNetWrapper import NNetWrapper
from AlphaZero.MCTS import MCTS
from AlphaZero.utils import dotdict


class AlphaZeroPlayer:
    def __init__(self, game, checkpoint_dir, num_sims):
        n1 = NNetWrapper(game)
        n1.load_checkpoint(os.path.join(checkpoint_dir), 'best.pth.tar')
        args1 = dotdict({'numMCTSSims': num_sims, 'cpuct': 1.0})
        self.mcts = MCTS(game, n1, args1)
        self.name = "AlphaZero"

    def play(self, board):
        return np.argmax(self.mcts.getActionProb(board, temp=0))


class MCTSPlayer:
    def __init__(self, game, depth):
        self.game = game
        self.depth = depth
        self.name = "MCTS"

    # Simulates a random playout from the current game board until the game ends
    @staticmethod
    def simulate(game, board, player):
        # Continue simulating moves while the game is ongoing
        cur_player = player
        b = np.array(board, order='K', copy=True)
        while game.check_win(b) == 0:
            # Get a list of valid moves
            valid_moves = game.get_valid_moves(b, cur_player)

            # Select a random move from the list of valid moves
            valid_moves = np.nonzero(valid_moves)[0]
            random_idx = np.random.randint(len(valid_moves))
            random_move = valid_moves[random_idx]
            # Place the move on the board without checking for a win
            b, still_turn = game.place_move(b, cur_player, random_move)
            # Switch to the other player
            if not still_turn:
                cur_player = -cur_player
        # Return the game result
        return game.check_win(b)

    # Monte Carlo Tree Search function
    def play(self, board):
        # Initialize the best move and best score
        best_move = None
        best_score = float('-inf')
        player = 1
        # new_board = np.copy(board)
        # Get a list of valid moves
        valid_moves = np.nonzero(self.game.get_valid_moves(board, 1))[0]
        # # If there's only one valid move, return it immediately
        if len(valid_moves) == 1:
            return valid_moves[0]

        # Loop through all valid moves
        for move in valid_moves:
            # Place the move on a copy of the board without checking for a win
            new_board, still_turn = self.game.place_move(np.array(board, order='K', copy=True), player, move)
            # Initialize the number of wins for this move
            wins = 0

            # Perform a specified number of simulations for this move
            for _ in range(self.depth):
                # Simulate a random playout and get the game result
                # simulation_result = self.simulate(self.game, new_board, player)
                # If the result is a win for the current player, increment the wins counter
                simulation_result = self.simulate(self.game,new_board, player)
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
        self.name = "Minimax"

    # MiniMax algorithm.
    def minimax(self, board, depth, player, isMaximizingPlayer, alpha, beta):
        # win_check = self.game.check_win(board)
        # if depth == 0 or (win_check == 1 or win_check == 2):
        if depth == 0 or self.game.get_game_ended(board, player) != 0:
            return self.game.evaluate(player, board)

        if isMaximizingPlayer:
            best_value = float('-inf')
            for move in self.game.get_valid_moves(board, player).nonzero()[0]:
                new_board, still_turn = self.game.place_move(board, player, move)
                if not still_turn:
                    player = -player
                value = self.minimax(new_board, depth - 1, player, still_turn, alpha, beta)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = float('inf')
            for move in self.game.get_valid_moves(board, player).nonzero()[0]:
                new_board, still_turn = self.game.place_move(board, player, move)
                if not still_turn:
                    player = -player
                value = self.minimax(new_board, depth - 1, player, still_turn, alpha, beta)
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
            new_board, still_turn = self.game.place_move(np.array(board, order='K', copy=True), player, move)
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
        self.name = "Human"

    def play(self, board):
        # if turn pass, skip turn
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


class RandomPlayer:
    def __init__(self, game):
        self.game = game
        self.name = "Random"

    def play(self, board):
        valid = self.game.get_valid_moves(board, 1)
        while True:
            valid_moves = self.game.get_valid_moves(board, 1)
            # Select a random move from the list of valid moves
            valid_moves = np.nonzero(valid_moves)[0]
            random_idx = np.random.randint(len(valid_moves))
            random_move = valid_moves[random_idx]
            if valid[random_move]:
                return random_move
