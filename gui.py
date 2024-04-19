# import tkinter as tk
# from tkinter import messagebox
# from gameplay.game_play_helpers import create_board, make_move, possible_moves, check_win
# from algorithms.minimax_algorithm import alpha_beta_search
# import threading
# import copy

import tkinter as tk
from tkinter import messagebox
from threading import Thread
import copy
from gameplay.game_play_helpers import create_board, make_move, possible_moves, check_win
from algorithms.minimax_algorithm import alpha_beta_search


class Connect4GUI:
    def __init__(self, master):
        self.master = master
        master.title("Connect 4")
        self.master.configure(bg='grey')  # Set background color for the window

        self.board = create_board()
        self.current_player = 'X'  # AI starts first
        self.buttons = [[None for _ in range(7)] for _ in range(6)]

        # Setting up the game board frame
        board_frame = tk.Frame(self.master, bg='grey')  # Dark blue background similar to traditional Connect 4 games
        board_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create a grid of buttons inside the frame
        for row in range(6):
            for col in range(7):
                button = tk.Button(board_frame, text='', font=('Helvetica', 14), height=2, width=4,
                                   command=lambda c=col: self.place_piece(c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button
                self.color_button(row, col, 'SystemButtonFace')  # Default color

        self.status_label = tk.Label(self.master, text="AI is thinking...", font=('Helvetica', 16), bg='navy', fg='white')
        self.status_label.grid(row=1, column=0)
        self.start_ai_move()

    def start_ai_move(self):
        thread = Thread(target=self.ai_move)
        thread.start()

    def place_piece(self, col):
        if col in possible_moves(self.board) and (self.current_player == 'O' or self.current_player == 'X'):
            self.board = make_move(self.board, col, self.current_player)
            self.update_board()
            self.switch_player()
            if self.current_player == 'X':
                self.status_label.config(text="AI is thinking...")
                thread = Thread(target=self.ai_move)
                thread.start()

    def update_board(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == 'O':  # Assuming 'O' is the red player
                    self.buttons[row][col].config(text="🟡")
                elif self.board[row][col] == 'X':  # Assuming 'X' is the yellow player
                    self.buttons[row][col].config(text="🔴")
                else:
                    self.buttons[row][col].config(text='')
                # self.buttons[row][col].config(text=self.board[row][col], bg='white' if self.board[row][col] == ' ' else 'red' if self.board[row][col] == 'O' else 'yellow')

    def color_button(self, row, col, color):
        self.buttons[row][col].config(bg=color)

    def ai_move(self):
        _, col = alpha_beta_search(copy.deepcopy(self.board), 'X')
        self.master.after(500, lambda: self.finalize_ai_move(col))

    def finalize_ai_move(self, col):
        self.place_piece(col)
        self.update_board()
        game_over, winner = check_win(self.board)
        if game_over:
            self.master.after(100, lambda: self.game_over(winner))

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'
        self.status_label.config(text=f"Player {self.current_player}'s turn")

    def game_over(self, winner):
        message = "It's a tie!" if winner is None else f"Player {winner} wins!"
        messagebox.showinfo("Game Over", message)
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = Connect4GUI(root)
    root.mainloop()