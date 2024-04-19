from database.models import SavedMove, Session
from gameplay.game_play_helpers import is_terminal, utility, possible_moves, make_move
import copy

def memoize_search(func):
    def wrapper(board, player):
        session = Session()
        board_str = str(board)  # Convert the board list to a string to hash
        found_move = session.query(SavedMove).filter_by(board_state=board_str).first()
        if found_move:
            return eval(found_move.move)  # Assuming move is stored as a string that can be evaluated back to a tuple
        else:
            result = func(board, player)
            new_move = SavedMove(board_state=board_str, move=str(result))
            session.add(new_move)
            session.commit()
            return result
    return wrapper

@memoize_search
def alpha_beta_search(board, current_player):
    max_depth = 6
    return max_value(board, float('-inf'), float('inf'), current_player, 0, max_depth)

def max_value(board, alpha, beta, player, depth, max_depth):
    if is_terminal(board) or depth == max_depth:
        return utility(board, player), None
    max_eval = float('-inf')
    best_move = None
    for move in possible_moves(board):
        copy_board = copy.deepcopy(board)
        new_board = make_move(copy_board, move, player)
        eval, _ = min_value(new_board, alpha, beta, player, depth + 1, max_depth)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
        if beta <= alpha:
            break
    return max_eval, best_move

def min_value(board, alpha, beta, player, depth, max_depth):
    if is_terminal(board) or depth == max_depth:
        return utility(board, player), None
    min_eval = float('inf')
    best_move = None
    for move in possible_moves(board):
        copy_board = copy.deepcopy(board)
        new_board = make_move(copy_board, move, 'O' if player == 'X' else 'X')
        eval, _ = max_value(new_board, alpha, beta, player, depth + 1, max_depth)
        if eval < min_eval:
            min_eval = eval
            best_move = move
        beta = min(beta, eval)
        if beta <= alpha:
            break
    return min_eval, best_move
