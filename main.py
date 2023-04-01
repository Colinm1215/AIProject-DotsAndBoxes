# This is a sample Python script.
import copy


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def read_gamestate(file_path):
    board = []
    f = open(file_path, "r")
    i = 0
    first_row_size = 0
    for x in f:
        if x == "\n":
            continue
        row = []
        for c in x:
            if c == "\n":
                continue
            row.append(c)
        while len(row) < first_row_size:
            row.append(" ")
        board.append(row)
        if i == 0:
            i = 1
            first_row_size = len(row)
    return board


def create_gameboard(size):
    size = size*2 + 1
    board = [[" "] * size for i in range(size)]
    i = 0
    while i < size:
        j = 0
        while j < size:
            board[i][j] = "O"
            j += 2
        i += 2
    return board


def print_board(board):
    for r in board:
        str = ""
        for i in range(len(r)):
            str = str + r[i]
        print(str)
    print()


def place_move(board, player, move_r, move_c):
    still_turn = False
    game_board = copy.deepcopy(board)
    if move_r % 2 == 0:
        if move_c % 2 == 0:
            return "Invalid Move"
        else:
            game_board[move_r][move_c] = "-"
        row_above = move_r - 2
        row_below = move_r + 2
        if row_above >= 0:
            if game_board[row_above][move_c] == "-":
                col_left = move_c - 1
                col_right = move_c + 1
                if col_left >= 0:
                    if game_board[move_r - 1][col_left] == "|":
                        if col_right < len(game_board[move_r]):
                            if game_board[move_r - 1][col_right] == "|":
                                game_board[move_r - 1][move_c] = player
                                still_turn = True
        if row_below < len(game_board):
            if game_board[row_below][move_c] == "-":
                col_left = move_c - 1
                col_right = move_c + 1
                if col_left >= 0:
                    if game_board[move_r + 1][col_left] == "|":
                        if col_right < len(game_board[move_r]):
                            if game_board[move_r + 1][col_right] == "|":
                                game_board[move_r + 1][move_c] = player
                                still_turn = True
    else:
        if move_c % 2 == 0:
            game_board[move_r][move_c] = "|"
        else:
            return "Invalid Move"
        col_left = move_c - 2
        col_right = move_c + 2
        if col_left >= 0:
            if game_board[move_r][col_left] == "|":
                row_above = move_r-1
                row_below = move_r+1
                if row_above >= 0:
                    if game_board[row_above][move_c - 1] == "-":
                        if row_below < len(game_board):
                            if game_board[row_below][move_c - 1] == "-":
                                game_board[move_r][move_c - 1] = player
                                still_turn = True
        if col_right < len(game_board[move_r]):
            if game_board[move_r][col_right] == "|":
                row_above = move_r-1
                row_below = move_r+1
                if row_above >= 0:
                    if game_board[row_above][move_c + 1] == "-":
                        if row_below < len(game_board):
                            if game_board[row_below][move_c + 1] == "-":
                                game_board[move_r][move_c + 1] = player
                                still_turn = True
    return game_board, still_turn

# returns 0 if board not finished
# returns 1 if player 1 wins
# returns 2 if player 2 wins
# returns 3 if a tie occurs
def check_win(board):
    size = (len(board)-1)/2
    r = 1
    player1_count = 0
    player2_count = 0
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

    if player2_count + player1_count != size*size:
        return 0
    else:
        if player1_count > player2_count:
            return 1
        elif player2_count > player1_count:
            return 2
        else:
            return 3


def evaluate(board, player):
    player1_count = 0
    player2_count = 0
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


def get_valid_moves(board):
    validMoves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if (row % 2 == 0):
                if (col % 2 != 0):
                    if board[row][col] == " ":
                        validMoves.append([row,col])
            else:
                if (col % 2 == 0):
                    if board[row][col] == " ":
                        validMoves.append([row,col])
    return validMoves


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
            next_player = "2" if player == "1" else "1"
            value = minimax(new_board, depth - 1, next_player, False, float('-inf'), float('inf'))
        if value > best_value:
            best_value = value
            best_move = move

    return best_move


if __name__ == '__main__':
    inp = input("Please enter the name of the gamestate file to read in, or enter \"new gamestate\" : ")
    board = []
    if inp == "new gamestate":
        size = int(input("Please enter the size of the new board : "))
        board = create_gameboard(size)
    else:
        board = read_gamestate(inp)

    depth = int(input("At what max_depth should the minimax algorithm search to find a move? : "))
    done = False
    turn = 1

    print_board(board)

    while not done:
        if turn % 2 == 0:
            player = "2"
            print("Player 2's turn!")
        else:
            print("Player 1's turn!")
            player = "1"
        player_move = get_best_move(board, depth, player)
        board, still_turn = place_move(board, player, player_move[0], player_move[1])
        print_board(board)
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


