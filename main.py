import time
import DotsAndBoxes as db

# The program begins by allowing the user to choose from a scenario gamestate or select a new gamestate (a new game).
# If a scenario is given, the user inputs the current turn for the given scenario.
# If a new game is selected, the user enters the board size.
# Finally, the user selects the max_depth the MiniMax algorithm should use during move selection.
# The game is then played out between two AI players.
# The game board is printed after each turn.
# The board is evaluated after each turn to determine if it is over. If so, a result is displayed.
# The time of each turn and overall game is tracked.
if __name__ == '__main__':
    inp = input("Please enter the name of the gamestate file to read in, or enter \"new\" : ")
    board = []
    turn_inp = "no"
    g = db.DotsAndBoxes(3)
    if inp == "new":
        size = int(input("Please enter the size of the new board : "))
        board = g.create_gameboard(size)
    else:
        turn_inp = input("Scenario Testing - Enter current turn number or enter 'no': ")
        board = g.read_gamestate(inp)

    player1_type = "none"
    depth_player1 = 0
    while player1_type == "none":
        player1_type = input("Please enter player 1's play type [manual, minimax, mcts] : ")
        if player1_type == "minimax":
            depth_player1 = int(input("At what max_depth should the minimax algorithm search to find a move? : "))
        elif player1_type == "mcts":
            depth_player1 = int(input("How many simulations should MCTS use to find a move? : "))
        elif player1_type == "manual":
            continue
        else:
            print("Invalid Type")
            player1_type = "none"

    player2_type = "none"
    depth_player2 = 0
    while player2_type == "none":
        player2_type = input("Please enter player 2's play type [manual, minimax, mcts] : ")
        if player2_type == "minimax":
            depth_player2 = int(input("At what max_depth should the minimax algorithm search to find a move? : "))
        elif player2_type == "mcts":
            depth_player2 = int(input("How many simulations should MCTS use to find a move? : "))
        elif player2_type == "manual":
            continue
        else:
            print("Invalid Type")
            player2_type = "none"

    done = False
    if turn_inp == 'no':
        turn = 1
    else:
        turn = int(turn_inp)
    g.print_board(board)
    game_start = time.perf_counter()

    while not done:
        turn_start = time.perf_counter()
        if turn % 2 == 0:
            print("Player 2's turn!")
            board, still_turn = g.switch_for_turn_type(board, 2, depth_player2, player2_type)
        else:
            print("Player 1's turn!")
            board, still_turn = g.switch_for_turn_type(board, 1, depth_player1, player1_type)

        g.print_board(board)
        turn_end = time.perf_counter()
        turn_time = round((turn_end - turn_start), 4)
        print('Turn time: ' + str(turn_time) + ' seconds' + '\n')
        print(g.completed_boxes)
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
