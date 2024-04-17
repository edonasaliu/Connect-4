from gameplay.game_play_helpers import create_board, show_board, make_move, possible_moves, check_win
from algorithms.minimax_algorithm import minimax
from database.models import init_db, Session, Game, Move

def best_move(board, player):
    best_eval = float('-inf')
    best_col = None
    for col in possible_moves(board):
        temp_board = [row[:] for row in board]
        make_move(temp_board, col, player)
        eval = minimax(temp_board, 4, float('-inf'), float('inf'), False)
        if eval > best_eval:
            best_eval = eval
            best_col = col
    return best_col

def main():
    init_db()  # Initialize the database
    session = Session()  # Create a session
    game = Game(winner=None)  # Start a new game
    session.add(game)
    session.commit()

    board = create_board()
    game_over = False
    current_player = 'X'  # AI

    while not game_over:
        show_board(board)
        if current_player == 'O':
            move = int(input("Your move (1-7): ")) - 1
            if move in possible_moves(board):
                board = make_move(board, move, 'O')
                session.add(Move(game_id=game.id, position=move, player='O'))
        else:
            move = best_move(board, 'X')
            board = make_move(board, move, 'X')
            session.add(Move(game_id=game.id, position=move, player='X'))
            print("AI plays at column:", move + 1)

        session.commit()

        if check_win(board)[0]:
            game_over = True
            game.winner = check_win(board)[1]
            show_board(board)
            print("Game Over. Winner:", game.winner)
            session.commit()
        
        current_player = 'O' if current_player == 'X' else 'X'

if __name__ == "__main__":
    main()
