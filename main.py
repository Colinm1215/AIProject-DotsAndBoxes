# This is a sample Python script.

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
    if move_r % 2 == 0:
        if move_c % 2 == 0:
            return "Invalid Move"
        else:
            board[move_r][move_c] = "-"
        row_above = move_r - 2
        row_below = move_r + 2
        if row_above >= 0:
            if board[row_above][move_c] == "-":
                col_left = move_c - 1
                col_right = move_c + 1
                if col_left >= 0:
                    if board[move_r - 1][col_left] == "|":
                        if col_right < len(board[move_r]):
                            if board[move_r - 1][col_right] == "|":
                                board[move_r - 1][move_c] = player
        if row_below < len(board):
            if board[row_below][move_c] == "-":
                col_left = move_c - 1
                col_right = move_c + 1
                if col_left >= 0:
                    if board[move_r + 1][col_left] == "|":
                        if col_right < len(board[move_r]):
                            if board[move_r + 1][col_right] == "|":
                                board[move_r + 1][move_c] = player
    else:
        if move_c % 2 == 0:
            board[move_r][move_c] = "|"
        else:
            return "Invalid Move"
        col_left = move_c - 2
        col_right = move_c + 2
        if col_left >= 0:
            if board[move_r][col_left] == "|":
                row_above = move_r-1
                row_below = move_r+1
                if row_above >= 0:
                    if board[row_above][move_c-1] == "-":
                        if row_below < len(board):
                            if board[row_below][move_c-1] == "-":
                                board[move_r][move_c-1] = player
        if col_right < len(board[move_r]):
            if board[move_r][col_right] == "|":
                row_above = move_r-1
                row_below = move_r+1
                if row_above >= 0:
                    if board[row_above][move_c+1] == "-":
                        if row_below < len(board):
                            if board[row_below][move_c+1] == "-":
                                board[move_r][move_c+1] = player

# returns 0 if board not finished
# returns 1 if player 1 wins
# returns 2 if player 2 wins
# returns 3 if a tie occurs
def check_win(board):
    size = len(board)
    r = 1
    player1_count = 0
    player2_count = 0
    while r < size:
        c = 1
        while c < size:
            if board[r][c] == "1":
                player1_count += 1
            elif board[r][c] == "2":
                player2_count += 1
            else:
                return 0
            c += 2
        r += 2
    if player2_count + player1_count != size - 1:
        return 0
    else:
        if player1_count > player2_count:
            return 1
        elif player2_count > player1_count:
            return 2
        else:
            return 3


if __name__ == '__main__':
    board = read_gamestate("scenario1.txt")
    print_board(board)
    print(check_win(board))
