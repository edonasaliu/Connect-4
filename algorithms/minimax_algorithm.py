from database.models import SavedMove, Session
from gameplay.game_play_helpers import is_terminal, utility, possible_moves, make_move
import copy

def memoize_search(func):
    """
    A decorator function that memoizes the results of a search algorithm.

    Args:
        func (function): The search algorithm function to be memoized.

    Returns:
        function: The memoized version of the search algorithm function.
    """
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
    """
    Performs alpha-beta search on the given Connect-4 board.

    Parameters:
    - board: The Connect-4 board state.
    - current_player: The player whose turn it is.

    Returns:
    - The best move for the current player.

    """
    max_depth = 6
    return max_value(board, float('-inf'), float('inf'), current_player, 0, max_depth)

def max_value(board, alpha, beta, player, depth, max_depth):
    """
    Calculates the maximum value and corresponding best move for the given board state using the minimax algorithm.

    Args:
        board (list): The current state of the game board.
        alpha (float): The alpha value for alpha-beta pruning.
        beta (float): The beta value for alpha-beta pruning.
        player (str): The player for whom the maximum value is being calculated.
        depth (int): The current depth of the search tree.
        max_depth (int): The maximum depth of the search tree.

    Returns:
        tuple: A tuple containing the maximum value and the corresponding best move.
    """
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
    """
    Calculates the minimum evaluation value and the best move for the given board state using the Minimax algorithm.

    Args:
        board (list): The current state of the game board.
        alpha (float): The alpha value for alpha-beta pruning.
        beta (float): The beta value for alpha-beta pruning.
        player (str): The player for whom the evaluation is being done.
        depth (int): The current depth of the search.
        max_depth (int): The maximum depth of the search.

    Returns:
        tuple: A tuple containing the minimum evaluation value and the best move.
    """
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
