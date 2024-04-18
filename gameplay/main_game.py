from algorithms.minimax_algorithm import alpha_beta_search
from gameplay.game_play_helpers import create_board, show_board, make_move, possible_moves, check_win
import copy

def main():
    board = create_board()
    game_over = False
    current_player = 'X'

    while not game_over:
        show_board(board)
        if current_player == 'O':
            move = int(input("Your move (1-7): ")) - 1
            if move in possible_moves(board):
                board = make_move(board, move, 'O')
        else:
            board_copy = copy.deepcopy(board)
            _, move = alpha_beta_search(board_copy, current_player)
            board = make_move(board, move, 'X')
            print("AI plays at column:", move + 1)

        game_over, winner = check_win(board)
        if game_over:
            show_board(board)
            print("Game Over. Winner:", winner)
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()