import numpy as np
from gameplay.game_play_helpers import is_terminal, evaluate_board, possible_moves, make_move, check_win

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in possible_moves(board):
            temp_board = make_move(np.copy(board), move, 'X')  # Assume 'X' is AI
            eval = minimax(temp_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves(board):
            temp_board = make_move(np.copy(board), move, 'O')  # Assume 'O' is human
            eval = minimax(temp_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return min_eval
