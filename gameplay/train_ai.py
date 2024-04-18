from algorithms.minimax_algorithm import alpha_beta_search
from gameplay.game_play_helpers import create_board, show_board, make_move, possible_moves, check_win, is_terminal
import copy
import time
import random


def generate_move(board, move_generation="normal"):
    if move_generation == "uniform":
        weights = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
    elif move_generation == "side_biased":
        weights = {0: 4, 1: 3, 2: 2, 3: 1, 4: 2, 5: 3, 6: 4}
    else:
        weights = {0: 1, 1: 2, 2: 3, 3: 4, 4: 3, 5: 2, 6: 1}

    moves = possible_moves(board)
    chance_list = []
    for move in moves:
        chance_list += [move] * weights[move]

    return random.choice(chance_list)


def main():
    num_sessions = int(input("How many sessions do you want to run?"))
    num_rounds = int(input("Set max number of turns for trainer:"))
    move_generation = input("Move distribution (uniform, normal, side_biased):")

    session_data = []
    num_sessions_completed = 0
    print("\nRunning session...")
    session_start_time = time.time()
    for _ in range(num_sessions):
        session_data.append(train_ai(num_rounds, move_generation))
        num_sessions_completed += 1
        completion_rate = round((num_sessions_completed*100) / num_sessions, 1)
        fill_bars = int(completion_rate/4)
        print(f"{completion_rate}% complete |{'='*fill_bars + ' '*(25 - fill_bars)}|", end="")
        print("\r", end="")

    total_ai_playing_time = 0
    w, d, l = 0, 0, 0

    print("\n")
    for i in range(len(session_data)):
        total_ai_playing_time += session_data[i][0]
        if session_data[i][1] == "W":
            w += 1
        elif session_data[i][1] == "D":
            d += 1
        elif session_data[i][1] == "L":
            l += 1

    total_session_time = time.time() - session_start_time

    print(f"FULL SESSION SUMMARY")
    print(f"Total AI playing time: {round(total_ai_playing_time, 3)} seconds")
    print(f"Total Session time: {round(total_session_time, 3)} seconds")
    print(f"Number of rounds played each game: {num_rounds} rounds")
    print(f"Win rate: {round((w*100)/num_sessions, 1)}%")
    print(f"Draw rate: {round((d*100)/num_sessions, 1)}%")
    print(f"Loss rate: {round((l*100)/num_sessions, 1)}%")
    print("\n")


def train_ai(rounds=10, move_generation="normal"):
    total_ai_time_spent = 0
    game_status = "D"
    trainer_turns_played = 0

    board = create_board()
    current_player = "X"

    while not is_terminal(board) and trainer_turns_played < rounds:
        if current_player == "O":
            user_input = generate_move(board, move_generation)
            board = make_move(board, user_input, 'X')
            trainer_turns_played += 1

        else:
            start = time.time()
            board_copy = copy.deepcopy(board)
            _, move = alpha_beta_search(board_copy, current_player)
            board = make_move(board, move, 'X')
            time_spent = time.time() - start
            total_ai_time_spent += time_spent

        if check_win(board)[0]:
            if current_player == "X":
                game_status = "W"
            else:
                game_status = "L"

        current_player = 'O' if current_player == 'X' else 'X'

    return total_ai_time_spent, game_status

if __name__ == "__main__":
    main()
