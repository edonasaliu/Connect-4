import numpy as np

def create_board():
    return np.full((6, 7), ' ', dtype=str)

def show_board(board):
    print("1 2 3 4 5 6 7")
    for row in board:
        print('|' + '|'.join(row) + '|')

def possible_moves(board):
    return [col for col in range(7) if board[0][col] == ' ']

def make_move(board, col, token):
    for r in reversed(range(6)):
        if board[r][col] == ' ':
            board[r][col] = token
            break
    return board

def check_win(board):
    # Horizontal, vertical, and diagonal checks simplified
    # Assume checks for 'X' and 'O' for simplicity
    for row in board:
        for col in range(4):
            if row[col] == row[col + 1] == row[col + 2] == row[col + 3] != ' ':
                return True, row[col]
    return False, None

def is_terminal(board):
    if any(check_win(board)):
        return True
    if all(board[0][col] != ' ' for col in range(7)):
        return True
    return False

def evaluate_board(board):
    # Simplistic evaluation function
    if check_win(board)[1] == 'X':
        return 100
    elif check_win(board)[1] == 'O':
        return -100
    return 0
