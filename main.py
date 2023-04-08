import copy
import time

global completed_boxes


# Reads in a given scenario game state.
def read_gamestate(file_path):
    board = []
    f = open(file_path, "r")
    first_row = f.readline()
    board = create_gameboard(len(first_row) - 1)
    global completed_boxes
    completed_boxes = [[0] *(len(first_row) - 1) for i in range((len(first_row) - 1))]
    print(board)
    f = open(file_path, "r")
    row = 0
    col = 0
    for x in f:
        if x == "\n" or x == "":
            continue
        x = x.strip("\n")
        for c in x:
            if c == "\n":
                continue
            if c == "1":
                board[row][col] = 1
            else:
                board[row][col] = 0
            col += 1
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
    for r in range(len(board)):
        if len(board[r]) == len(board[0]):
            type = "row"
            stri = "O"
        else:
            type = "col"
            stri = ""
        for i in range(len(board[r])):
            if board[r][i] == 1:
                if type == "row":
                    stri += "-O"
                else:
                    if i > len(completed_boxes[0]) or r > len(completed_boxes):
                        stri += "| "
                        continue
                    c_box_index_r = r-1
                    c_box_index_c = i
                    if c_box_index_r < 0:
                        c_box_index_r = 0
                    if completed_boxes[c_box_index_r][c_box_index_c] == 0:
                        stri += "| "
                    else:
                        stri += "|" + str(completed_boxes[c_box_index_r][c_box_index_c])
            else:
                if type == "row":
                    stri += " O"
                else:
                    stri += "  "

        print(stri)
    print()

def check_completed_box(board, move_r, move_c, player):
    if move_r % 2 == 0:
        if move_r > 0:
            if (
                    board[move_r - 1][move_c] == 1
                    and board[move_r - 1][move_c - 1] == 1
                    and board[move_r - 2][move_c] == 1
            ):
                completed_boxes[(move_r - 2) // 2][(move_c) // 2] = player

        if move_r < len(board) - 2:
            if (
                    board[move_r + 1][move_c] == 1
                    and board[move_r + 1][move_c - 1] == 1
                    and board[move_r + 2][move_c] == 1
            ):
                completed_boxes[move_r // 2][(move_c) // 2] = player

    elif move_r % 2 != 0:
        if move_c > 0:
            if (
                    board[move_r][move_c - 2] == 1
                    and board[move_r - 1][move_c - 1] == 1
                    and board[move_r + 1][move_c - 1] == 1
            ):
                completed_boxes[(move_r - 1) // 2][(move_c - 2) // 2] = player

        if move_c < len(board[0]) - 2:
            if (
                    board[move_r][move_c + 2] == 1
                    and board[move_r - 1][move_c + 1] == 1
                    and board[move_r + 1][move_c + 1] == 1
            ):
                completed_boxes[(move_r - 1) // 2][move_c // 2] = player


# Checks if moves are valid and how they should be made (horizontal or vertical). Adds player # to completed boxes.
def place_move(board, player, move_r, move_c):
    global completed_boxes
    game_board = copy.deepcopy(board)
    game_board[move_r][move_c] = 1
    print(game_board)

    still_turn = check_completed_box(board, move_r, move_c, int(player))
    print(completed_boxes)
    return game_board



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
        if player == "1":
            return float('inf')
        else:
            return float('-inf')
    if check_win(board) == 2:
        if player == "2":
            return float('inf')
        else:
            return float('-inf')
    if check_win(board) == 3:
        return 0

    for row in range(len(board)):
        for col in range(len(board[0])):
            if (row % 2 != 0):
                if (col % 2 != 0):
                    if board[row][col] == "1":
                        player1_count += 1
                    elif board[row][col] == "2":
                        player2_count += 1
            else:
                if (col % 2 == 0):
                    if board[row][col] == "1":
                        player1_count += 1
                    elif board[row][col] == "2":
                        player2_count += 1

    if player == "1":
        return player1_count - player2_count
    else:
        return player2_count - player1_count


# Returns all remaining valid moves available to a player.
def get_valid_moves(board):
    validMoves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if (row % 2 == 0):
                if (col % 2 != 0):
                    if board[row][col] == 0:
                        validMoves.append([row, col])
            else:
                if (col % 2 == 0):
                    if board[row][col] == 0:
                        validMoves.append([row, col])
    return validMoves


# MiniMax algorithm.
def minimax(board, depth, player, isMaximizingPlayer, alpha, beta):
    win_check = check_win(board)
    if depth == 0 or (win_check == 1 or win_check == 2):
        return evaluate(board, player)

    if isMaximizingPlayer:
        best_value = float('-inf')
        for move in get_valid_moves(board):
            new_board, still_turn = place_move(board, player, move[0], move[1])
            if still_turn:
                value = minimax(new_board, depth - 1, player, True, alpha, beta)
            else:
                next_player = "2" if player == "1" else "1"
                value = minimax(new_board, depth - 1, next_player, False, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float('inf')
        for move in get_valid_moves(board):
            new_board, still_turn = place_move(board, player, move[0], move[1])
            if still_turn:
                value = minimax(new_board, depth - 1, player, False, alpha, beta)
            else:
                next_player = "2" if player == "1" else "1"
                value = minimax(new_board, depth - 1, next_player, True, alpha, beta)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


# Selects the best move from the list of available valid moves using the MiniMax algorithm.
def get_best_move(board, depth, player):
    game_board = copy.deepcopy(board)
    best_move = None
    best_value = float('-inf')

    move_list = get_valid_moves(game_board)

    if len(move_list) == 1:
        return move_list[0]

    for move in move_list:
        new_board, still_turn = place_move(game_board, player, move[0], move[1])
        if still_turn:
            value = minimax(new_board, depth - 1, player, True, float('-inf'), float('inf'))
        else:
            next_player = 2 if player == 1 else 1
            value = minimax(new_board, depth - 1, next_player, False, float('-inf'), float('inf'))
        if value > best_value:
            best_value = value
            best_move = move

    return best_move


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

    depth = int(input("At what max_depth should the minimax algorithm search to find a move? : "))
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
            player = "2"
            print("Player 2's turn!")
        else:
            print("Player 1's turn!")
            player = "1"
        player_move_row = int(input("Enter Move Row : "))
        player_move_col = int(input("Enter Move Col : "))
        valid_moves = get_valid_moves(board)
        in_valid_moves = False
        for move in valid_moves:
            if player_move_row == move[0] and player_move_col == move[1]:
                in_valid_moves = True
        if in_valid_moves:
            print("move valid")
        board = place_move(board, player, player_move_row, player_move_col)
        print_board(board)
        still_turn = False
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
