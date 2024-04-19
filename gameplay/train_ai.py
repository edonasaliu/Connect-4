from algorithms.minimax_algorithm import alpha_beta_search
from gameplay.game_play_helpers import create_board, make_move, possible_moves, check_win, is_terminal
import copy
import time
import random


import random

def generate_move(board, move_generation="binomial"):
    """
    Generates a move based on the given board and move generation strategy.

    Args:
        board (list): The current game board.
        move_generation (str, optional): The move generation strategy. Defaults to "binomial".

    Returns:
        int: The generated move.

    Raises:
        KeyError: If an invalid move generation strategy is provided.
    """
    if move_generation == "uniform":
        weights = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
    elif move_generation == "skewed":
        weights = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 1}
    else:
        weights = {0: 1, 1: 2, 2: 3, 3: 4, 4: 3, 5: 2, 6: 1}

    moves = possible_moves(board)
    chance_list = []
    for move in moves:
        chance_list += [move] * weights[move]

    return random.choice(chance_list)


def main():
    """
    Function to train an AI by running multiple sessions of gameplay.

    This function prompts the user for the number of training sessions, the maximum number of turns,
    and the playing strategy for the trainer. It then runs the specified number of sessions, 
    collects data on each session, and calculates various statistics based on the collected data.

    Parameters:
    None

    Returns:
    None
    """
    n_sessions = int(input("Number of training sessions: "))
    max_turn = int(input("Set max number of turns: "))
    playing_strategy = input("Pick trainer (uniform, binomial, skewed): ")

    data = []
    sessions_finished = 0
    print("\nRunning session...")
    session_start_time = time.time()
    for _ in range(n_sessions):
        data.append(train_ai(max_turn, playing_strategy))
        sessions_finished += 1
        completion_rate = round((sessions_finished*100) / n_sessions, 1)
        fill_bars = int(completion_rate/4)
        print(f"{completion_rate}% complete |{'='*fill_bars + ' '*(25 - fill_bars)}|", end="")
        print("\r", end="")

    total_time = 0
    outcomes = {"w": 0, "d": 0, "l": 0}

    print("\n")
    for i in range(len(data)):
        total_time += data[i][0]
        outcome = data[i][1]
        outcomes[outcome] += 1

    total_session_time = time.time() - session_start_time

    print(f"TRAINING SESSION RESULTS:")
    print(f"Trainer: {playing_strategy}")
    print(f"Total AI playing time: {round(total_time, 3)} seconds")
    print(f"Total Session time: {round(total_session_time, 3)} seconds")
    print(f"Turns per player: {max_turn}")
    print(f"Win rate: {round((outcomes['w']*100)/n_sessions, 1)}%")
    print(f"Draw rate: {round((outcomes['d']*100)/n_sessions, 1)}%")
    print(f"Loss rate: {round((outcomes['l']*100)/n_sessions, 1)}%")
    print("\n")


def train_ai(rounds=10, move_generation="normal"):
    """
    Trains an AI by playing rounds of the game against itself.

    Parameters:
    - rounds (int): The number of rounds to play. Default is 10.
    - move_generation (str): The method used to generate moves for the AI. Default is "normal".

    Returns:
    - total_ai_time_spent (float): The total time spent by the AI in making moves.
    - game_status (str): The status of the game after training. Possible values are "w" (win), "l" (loss), or "d" (draw).
    """
    total_ai_time_spent = 0
    game_status = "d"
    trainer_turns_played = 0

    board = create_board()
    curr_player = "X"

    while not is_terminal(board) and trainer_turns_played < rounds:
        if curr_player == "O":
            dummy_ai_move = generate_move(board, move_generation)
            board = make_move(board, dummy_ai_move, 'O')
            trainer_turns_played += 1

        else:
            start = time.time()
            board_copy = copy.deepcopy(board)
            _, move = alpha_beta_search(board_copy, curr_player)
            board = make_move(board, move, 'X')
            time_spent = time.time() - start
            total_ai_time_spent += time_spent

        if check_win(board)[0]:
            if curr_player == "X":
                game_status = "w"
            else:
                game_status = "l"

        curr_player = 'O' if curr_player == 'X' else 'X'

    return total_ai_time_spent, game_status

if __name__ == "__main__":
    main()
