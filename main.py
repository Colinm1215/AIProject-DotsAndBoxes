# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def read_gamestate(file_path):

def create_gameboard(size):
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


if __name__ == '__main__':
    player_input_size = 3
    board = create_gameboard((player_input_size*2)-1)
    board[2][1] = "-"
    board[2][3] = "-"
    board[1][0] = "|"
    board[1][4] = "|"
    board[0][1] = "-"
    board[0][3] = "-"
    print_board(board)
    place_move(board, "1", 1, 2)
    print_board(board)