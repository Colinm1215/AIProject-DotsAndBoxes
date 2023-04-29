import time
import logging

import numpy as np

from Players import MinimaxPlayer, MCTSPlayer, HumanPlayer
from DotsAndBoxes import DotsAndBoxesGame as db
log = logging.getLogger(__name__)

if __name__ == '__main__':
    size = 5
    g = db(size)
    # board = g.read_gamestate("scenario1-3.1-matrix.txt")
    board = g.create_board(size)
    depth_player1 = 10
    player1 = MinimaxPlayer(g, depth_player1).play
    depth_player2 = 600
    player2 = MCTSPlayer(g, depth_player2).play
    turn = 0

    done = False
    game_start = time.perf_counter()
    players = [player2, None, player1]
    curPlayer = 1
    while not g.get_game_ended(board, curPlayer):
        turn_start = time.perf_counter()
        action = players[curPlayer + 1](g.get_canonical_form(np.copy(board), curPlayer))
        print(action)
        # valids = g.get_valid_moves(g.get_canonical_form(board, curPlayer), 1)
        board, curPlayer = g.get_next_state(board, curPlayer, action)

        print(board)
        # g.display_board(board)
        turn_end = time.perf_counter()
        turn_time = round((turn_end - turn_start), 4)
        print('Turn time: ' + str(turn_time) + ' seconds' + '\n')
        win_check = g.check_win(board)

        if win_check > 0:
            done = True
        if win_check == 1:
            print("Player 1 has won the game!")
        elif win_check == 2:
            print("Player 2 has won the game!")
        elif win_check == 3:
            print("The game has been tied!")
        turn += 1

    print("Game over: Turn ", str(turn), "Result ", str(g.get_game_ended(board, 1)))
    game_end = time.perf_counter()
    game_time = round((game_end - game_start), 3)
    print('Game time: ' + str(game_time) + ' seconds' + '\n')

