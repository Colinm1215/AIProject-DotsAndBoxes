import logging
import time

import numpy as np
from tqdm import tqdm

log = logging.getLogger(__name__)


class Arena:
    """
    An Arena class where any 2 agents can be pitted against each other.
    """

    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False, log_data=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        cur_player = 1
        board = self.game.create_board(self.game.n)
        game_start, game_end, turn_start, turn_end = 0, 0, 0, 0
        turn_times = []
        if log_data:
            game_start = time.perf_counter()
            turn_times = np.zeros(self.game.n * 20)
        it = 0
        while self.game.get_game_ended(board, cur_player) == 0:
            it += 1
            if verbose:
                assert self.display
                print("Turn ", str(it), "Player ", str(cur_player))
                self.display(self.game, board)

            if log_data:
                turn_start = time.perf_counter()

            action = players[cur_player + 1](self.game.get_canonical_form(board, cur_player))

            if log_data:
                turn_end = time.perf_counter()
                turn_time = round((turn_end - turn_start), 4)
                turn_times = np.insert(turn_times, it - 1, turn_time)

            valids = self.game.get_valid_moves(self.game.get_canonical_form(board, cur_player), 1)
            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, cur_player = self.game.get_next_state(board, cur_player, action, True)
        if verbose:
            assert self.display
            print("")
            self.display(self.game, board)
            print("Game over: Turn ", str(it), "Result ", str(self.game.get_game_ended(board, 1)))
        if log_data:
            game_end = time.perf_counter()
            game_time = round((game_end - game_start), 4)
            turn_times = turn_times[:it]
            s1, s2 = self.game.get_score(board)
            margin = max(s1, s2) - min(s1, s2)
            return cur_player * self.game.get_game_ended(board, cur_player), np.mean(turn_times[::2]), np.mean(
                turn_times[1::2]), game_time, margin
        else:
            return cur_player * self.game.get_game_ended(board, cur_player)

    def playGames(self, num, verbose=False, log_data=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        one_won, two_won, draws = 0, 0, 0
        avg_turn_p1 = []
        avg_turn_p2 = []
        avg_game_time = []
        avg_margin = []
        if log_data:
            avg_turn_p1 = np.zeros(num)
            avg_turn_p2 = np.zeros(num)
            avg_game_time = np.zeros(num)
            avg_margin = np.zeros(num)
        for i in tqdm(range(num), desc="Arena.playGames (1)"):
            if log_data:
                game_result, avg_turn1, avg_turn2, game_time, margin = self.playGame(verbose=verbose, log_data=log_data)
                avg_turn_p1 = np.insert(avg_turn_p1, i, avg_turn1)
                avg_turn_p2 = np.insert(avg_turn_p2, i, avg_turn2)
                avg_game_time = np.insert(avg_game_time, i, game_time)
                avg_margin = np.insert(avg_margin, i, margin)
            else:
                game_result = self.playGame(verbose=verbose)
            if game_result == 1:
                one_won += 1
            elif game_result == -1:
                two_won += 1
            else:
                draws += 1
        self.player1, self.player2 = self.player2, self.player1

        for i in tqdm(range(num), desc="Arena.playGames (2)"):
            if log_data:
                game_result, avg_turn1, avg_turn2, game_time, margin = self.playGame(verbose=verbose, log_data=log_data)
                avg_turn_p1 = np.insert(avg_turn_p1, i + num, avg_turn2)
                avg_turn_p2 = np.insert(avg_turn_p2, i + num, avg_turn1)
                avg_game_time = np.insert(avg_game_time, i + num, game_time)
                avg_margin = np.insert(avg_margin, i + num, margin)
            else:
                game_result = self.playGame(verbose=verbose)
            if game_result == -1:
                one_won += 1
            elif game_result == 1:
                two_won += 1
            else:
                draws += 1

        if log_data:
            return one_won, two_won, draws, np.trim_zeros(avg_turn_p1), np.trim_zeros(avg_turn_p2), np.trim_zeros(
                avg_game_time), np.trim_zeros(avg_margin)
        else:
            return one_won, two_won, draws
