import copy
import time
import random

global completed_boxes


# Reads in a given scenario game state.
def read_gamestate(file_path):
    f = open(file_path, "r")
    first_row = f.readline()
    board = create_gameboard(len(first_row) - 2)
    global completed_boxes
    completed_boxes = [[0] * (len(first_row) - 2) for i in range((len(first_row) - 2))]
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
            #Shouldn't be needed
            #print_board(board)
        col = 0
        row += 1

    return board


# Creates a new gamestate of a size selected by the user. Used if no scenario is given.
def create_gameboard(size):
    o_size = size
    global completed_boxes
    completed_boxes = [[0] * o_size for i in range(o_size)]
    size = size * 2 + 1
    board = []
    for i in range(size):
        if i % 2 == 0:
            board.append([0] * o_size)
        else:
            board.append([0] * (o_size + 1))
    return board


# Prints the game board.
def print_board(board):
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
                        if completed_boxes[(row - 1) // 2][col] == 0:
                            stri += "| "
                        else:
                            stri += "|" + str(completed_boxes[(row - 1) // 2][col])
                    else:
                        stri += "|"
            else:
                if type == "row":
                    stri += " O"
                else:
                    stri += "  "
        print(stri)
    print()


def check_completed_box(board, move_r, move_c, player, pri):
    global completed_boxes
    completed_boxes_temp = copy.deepcopy(completed_boxes)
    still_turn = False
    # Check if the current move is on a horizontal line
    if move_r % 2 == 0:
        # Check if there's a row above the current move
        if move_r > 0:
            # Check if there's a completed box above the current move
            if (
                    board[move_r - 1][move_c + 1] == 1  # Line to the right and above the current move
                    and board[move_r - 1][move_c] == 1  # Line above the current move
                    and board[move_r - 2][move_c] == 1  # Line to the left and above the current move
            ):
                # Update the completed_boxes entry for the box above the current move
                completed_boxes_temp[(move_r - 2) // 2][move_c] = player
                still_turn = True
        # Check if there's a row below the current move
        if move_r < len(board) - 2:
            # Check if there's a completed box below the current move
            if (
                    board[move_r + 1][move_c + 1] == 1  # Line to the right and below the current move
                    and board[move_r + 1][move_c] == 1  # Line below the current move
                    and board[move_r + 2][move_c] == 1  # Line to the left and below the current move
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
                    board[move_r][move_c - 1] == 1  # Line to the left of the current move
                    and board[move_r - 1][move_c - 1] == 1  # Line above and to the left of the current move
                    and board[move_r + 1][move_c - 1] == 1  # Line below and to the left of the current move
            ):
                # Update the completed_boxes entry for the box to the left of the current move
                completed_boxes_temp[(move_r - 1) // 2][move_c-1] = player
                still_turn = True
        # Check if there's a column to the right of the current move
        if move_c <= len(board[move_r]) - 2:
            # Check if there's a completed box to the right of the current move
            if (
                    board[move_r][move_c + 1] == 1  # Line to the right of the current move
                    and board[move_r - 1][move_c] == 1  # Line above and to the right of the current move
                    and board[move_r + 1][move_c] == 1  # Line below and to the right of the current move
            ):
                # Update the completed_boxes entry for the box to the right of the current move
                completed_boxes_temp[(move_r - 1) // 2][move_c] = player
                still_turn = True

    if pri:
        completed_boxes = completed_boxes_temp
    return still_turn


# Checks if moves are valid and how they should be made (horizontal or vertical). Adds player # to completed boxes.
def place_move(board, player, move_r, move_c, print):
    global completed_boxes
    game_board = copy.deepcopy(board)
    game_board[move_r][move_c] = 1

    still_turn = check_completed_box(board, move_r, move_c, player, print)
    return game_board, still_turn


# Checks if the game is finished and if so, who the winner is.
# Returns 0 if board not finished.
# Returns 1 if player 1 wins.
# Returns 2 if player 2 wins.
# Returns 3 if a tie occurs.
def check_win(board):
    size = (len(board) - 1) / 2
    player1_count = 0
    player2_count = 0
    for row in completed_boxes:
        for box in row:
            if box == 1:
                player1_count += 1
            elif box == 2:
                player2_count += 1

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
def evaluate(board, player):
    player1_count = 0
    player2_count = 0
    if check_win(board) == 1:
        if player == 1:
            return float('inf')
        else:
            return float('-inf')
    if check_win(board) == 2:
        if player == 2:
            return float('inf')
        else:
            return float('-inf')
    if check_win(board) == 3:
        return 0

    for row in completed_boxes:
        for col in row:
            if col == 1:
                player1_count += 1
            elif col == 2:
                player2_count += 1

    if player == 1:
        return player1_count - player2_count
    else:
        return player2_count - player1_count


# Returns all remaining valid moves available to a player.
def get_valid_moves(board):
    validMoves = []
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 0:
                validMoves.append([r,c])
    return validMoves


# MiniMax algorithm.
def minimax(board, depth, player, isMaximizingPlayer, alpha, beta):
    win_check = check_win(board)
    if depth == 0 or (win_check == 1 or win_check == 2):
        return evaluate(board, player)

    if isMaximizingPlayer:
        best_value = float('-inf')
        for move in get_valid_moves(board):
            new_board, still_turn = place_move(board, player, move[0], move[1], False)
            if still_turn:
                value = minimax(new_board, depth - 1, player, True, alpha, beta)
            else:
                next_player = 2 if player == 1 else 1
                value = minimax(new_board, depth - 1, next_player, False, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float('inf')
        for move in get_valid_moves(board):
            new_board, still_turn = place_move(board, player, move[0], move[1], False)
            if still_turn:
                value = minimax(new_board, depth - 1, player, False, alpha, beta)
            else:
                next_player = 2 if player == 1 else 1
                value = minimax(new_board, depth - 1, next_player, True, alpha, beta)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


# Selects the best move from the list of available valid moves using the MiniMax algorithm.
def get_best_move_minimax(board, depth, player):
    game_board = copy.deepcopy(board)
    best_move = None
    best_value = float('-inf')

    move_list = get_valid_moves(game_board)

    if len(move_list) == 1:
        return move_list[0]

    for move in move_list:
        new_board, still_turn = place_move(game_board, player, move[0], move[1], False)
        if still_turn:
            value = minimax(new_board, depth - 1, player, True, float('-inf'), float('inf'))
        else:
            next_player = 2 if player == 1 else 1
            value = minimax(new_board, depth - 1, next_player, False, float('-inf'), float('inf'))
        if value >= best_value:
            best_value = value
            best_move = move

    return best_move


def in_valid_moves(move_r, move_c, game_board):
    valid_moves = get_valid_moves(game_board)
    valid = False
    for move in valid_moves:
        if move_r == move[0] and move_c == move[1]:
            valid = True

    return valid


# Simulates a random playout from the current game board until the game ends
def simulate(board, player):
    # Continue simulating moves while the game is ongoing
    while check_win(board) == 0:
        # Get a list of valid moves
        valid_moves = get_valid_moves(board)
        # Select a random move from the list of valid moves
        if len(valid_moves) == 1:
            return valid_moves[0]
        random_move = random.choice(valid_moves)
        # Extract row and column from the selected move
        move_r, move_c = random_move
        # Place the move on the board without checking for a win
        board, _ = place_move(board, player, move_r, move_c, False)
        # Switch to the other player
        player = 2 if player == 1 else 1
    # Return the game result (1, 2, or 3)
    return check_win(board)


# Monte Carlo Tree Search function
def mcts(board, player, num_simulations):
    # Initialize the best move and best score
    best_move = None
    best_score = float('-inf')

    # Get a list of valid moves
    valid_moves = get_valid_moves(board)

    # If there's only one valid move, return it immediately
    if len(valid_moves) == 1:
        return valid_moves[0]

    # Loop through all valid moves
    for move in valid_moves:
        # Extract row and column from the current move
        move_r, move_c = move
        # Place the move on a copy of the board without checking for a win
        new_board, _ = place_move(copy.deepcopy(board), player, move_r, move_c, False)
        # Initialize the number of wins for this move
        wins = 0

        # Perform a specified number of simulations for this move
        for _ in range(num_simulations):
            # Simulate a random playout and get the game result
            simulation_result = simulate(copy.deepcopy(new_board), player)
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


def perform_turn_manual(board, player):
    player_move_row = int(input("Enter Move Row : "))
    player_move_col = int(input("Enter Move Col : "))
    while not in_valid_moves(player_move_row, player_move_col, board):
      print("Invalid Move")
      player_move_row = int(input("Enter Move Row : "))
      player_move_col = int(input("Enter Move Col : "))

    print("Placing at ", [player_move_row, player_move_col])
    return place_move(board, player, player_move_row, player_move_col, True)


def perform_turn_minimax(board, player, depth):
    move = get_best_move_minimax(board, depth, player)

    print("Placing at ", move)
    return place_move(board, player, move[0], move[1], True)


def perform_turn_mcts(board, player, depth):
    move = mcts(board, player, depth)

    print("Placing at ", move)
    return place_move(board, player, move[0], move[1], True)


def switch_for_turn_type(board, player, depth, type):
    if type == "minimax":
        return perform_turn_minimax(board, player, depth)
    elif type == "mcts":
        return perform_turn_mcts(board, player, depth)
    elif type == "manual":
        return perform_turn_manual(board, player)
    else:
        return None, False





# The program begins by allowing the user to choose from a scenario gamestate or select a new gamestate (a new game).
# If a scenario is given, the user inputs the current turn for the given scenario.
# If a new game is selected, the user enters the board size.
# Finally, the user selects the max_depth the MiniMax algorithm should use during move selection.
# The game is then played out between two AI players.
# The game board is printed after each turn.
# The board is evaluated after each turn to determine if it is over. If so, a result is displayed.
# The time of each turn and overall game is tracked.
if __name__ == '__main__':
    inp = input("Please enter the name of the gamestate file to read in, or enter \"new gamestate\" : ")
    board = []
    turn_inp = "no"
    if inp == "new gamestate":
        size = int(input("Please enter the size of the new board : "))
        board = create_gameboard(size)
    else:
        turn_inp = input("Scenario Testing - Enter current turn number or enter 'no': ")
        board = read_gamestate(inp)

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
    print_board(board)
    game_start = time.perf_counter()

    while not done:
        turn_start = time.perf_counter()
        if turn % 2 == 0:
            print("Player 2's turn!")
            board, still_turn = switch_for_turn_type(board, 2, depth_player2, player2_type)
        else:
            print("Player 1's turn!")
            board, still_turn = switch_for_turn_type(board, 1, depth_player1, player1_type)

        print_board(board)
        turn_end = time.perf_counter()
        turn_time = round((turn_end - turn_start), 4)
        print('Turn time: ' + str(turn_time) + ' seconds' + '\n')
        win_check = check_win(board)

        if (win_check > 0):
            done = True
        if (win_check == 1):
            print("Player 1 has won the game!")
        elif (win_check == 2):
            print("Player 2 has won the game!")
        elif (win_check == 3):
            print("The game has been tied!")
        if not still_turn:
            turn += 1

    game_end = time.perf_counter()
    game_time = round((game_end - game_start), 3)
    print('Game time: ' + str(game_time) + ' seconds' + '\n')
