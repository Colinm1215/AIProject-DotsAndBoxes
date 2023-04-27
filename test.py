import time

import numpy as np

from DotsAndBoxes import DotsAndBoxesGame as db

if __name__ == '__main__':
    size = 3
    g = db(size)
    board = g.create_gameboard(size)
    player1_type = "minimax"
    depth_player1 = 7
    player2_type = "mcts"
    depth_player2 = 5000
    turn = 1

    done = False
    game_start = time.perf_counter()
    while not done:
        turn_start = time.perf_counter()
        if turn % 2 == 0:
            # print("Player 2's turn!")
            board, still_turn, _ = g.switch_for_turn_type(board, 2, depth_player2, player2_type)
        else:
            # print("Player 1's turn!")
            board, still_turn, _ = g.switch_for_turn_type(board, 1, depth_player1, player1_type)

        print(board)
        # g.display_board(board)
        turn_end = time.perf_counter()
        turn_time = round((turn_end - turn_start), 4)
        # print('Turn time: ' + str(turn_time) + ' seconds' + '\n')
        # print(g.completed_boxes)
        win_check = g.check_win(board)

        if win_check > 0:
            done = True
        if win_check == 1:
            print("Player 1 has won the game!")
        elif win_check == 2:
            print("Player 2 has won the game!")
        elif win_check == 3:
            print("The game has been tied!")
        if not still_turn:
            turn += 1

    game_end = time.perf_counter()
    game_time = round((game_end - game_start), 3)
    print('Game time: ' + str(game_time) + ' seconds' + '\n')

