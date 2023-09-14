"""
Tic Tac Toe Game
Copyright (C) 2023 Mike Vermeer
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

This program is a simple implementation of the game Tic Tac Toe. It supports both single player and two players mode.
The single player mode has two difficulty options: easy and hard. The easy AI randomly selects an empty square,
while the hard AI uses the minimax algorithm to determine the optimal move.
"""

import tkinter as tk
from tkinter import messagebox
from random import choice
import copy

class TicTacToe:
    """
    TicTacToe is a class that represents a game of Tic Tac Toe. 
    The board is represented as a list of 9 elements, where each element can be 'X', 'O', or '' (empty).
    The game is either player vs player or player vs AI depending on the ai_difficulty argument passed to the constructor.
    """

    def __init__(self, ai_difficulty=None):
        """
        Constructor for the TicTacToe class. Initializes a new game of Tic Tac Toe.
        """

        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')

        self.window.configure(background='white')

        self.board = ['' for _ in range(9)]

        self.buttons = [tk.Button(self.window, width=15, height=5, command=lambda i=i : self.on_click(i), 
                                  font=('Helvetica', '20'), bg='sky blue', activebackground='deep sky blue') for i in range(9)]

        self.current_player = 'X'

        self.ai_difficulty = ai_difficulty

        for i in range(3):
            for j in range(3):
                self.buttons[i * 3 + j].grid(row=i, column=j, padx=5, pady=5)

        if ai_difficulty and self.ai_difficulty == 'O':
            self.window.after(1000, self.ai_move)

        self.window.mainloop()

    def on_click(self, cell):
        """
        Handles click events on the game board. Marks the clicked cell with the current player's mark if the cell is empty and the game is not over.
        """

        if self.board[cell] == '' and not self.check_win():
            self.board[cell] = self.current_player
            self.buttons[cell].config(text=self.current_player)
            win = self.check_win()
            if win:
                messagebox.showinfo("Game Over", f"{win} wins!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O' and self.ai_difficulty:
                    self.lock_buttons()
                    self.window.after(1000, self.ai_move)

    def check_win(self):
        """
        Checks if the game is over (either a player has won or the game is a draw).
        """

        winning_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for pos in winning_positions:
            values = [self.board[i] for i in pos]
            if values == ['X', 'X', 'X']:
                return 'X'
            if values == ['O', 'O', 'O']:
                return 'O'
        if '' not in self.board:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.window.quit()
        return None

    def ai_move(self):
        """
        Determines the AI's move and applies it to the board. The AI either selects an empty cell randomly (for easy mode) or uses the minimax algorithm (for hard mode).
        """
        if self.ai_difficulty == 'easy':
            empty_cells = [i for i, x in enumerate(self.board) if x == '']
            if empty_cells:
                self.on_click(choice(empty_cells))
        else:
            if len(self.available_moves(self.board)) == 9:
                square = choice(self.available_moves(self.board))
            else:
                _, square = self.minimax(copy.deepcopy(self.board), 'O')
            self.on_click(square)
        self.unlock_buttons()

    def available_moves(self, board):
        """
        Returns a list of the indexes of the empty cells in the specified board.
        """

        return [i for i, x in enumerate(board) if x == '']

    def minimax(self, board, player):
        """
        Minimax algorithm for determining the optimal move for the AI in hard mode.
        """

        available_moves = self.available_moves(board)

        if self.check_win_in_board(board) == 'X':
            return -1, None
        elif self.check_win_in_board(board) == 'O':
            return 1, None
        elif not available_moves:
            return 0, None

        best_score = -float('inf') if player == 'O' else float('inf')
        best_move = None

        for move in available_moves:
            board[move] = player
            score, _ = self.minimax(copy.deepcopy(board), 'X' if player == 'O' else 'O')
            board[move] = ''
            if player == 'O':
                if score > best_score:
                    best_score, best_move = score, move
            else:
                if score < best_score:
                    best_score, best_move = score, move

        return best_score, best_move

    def check_win_in_board(self, board):
        """
        Checks if a player has won or the game is a draw for a specified board.
        """

        winning_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for pos in winning_positions:
            values = [board[i] for i in pos]
            if values == ['X', 'X', 'X']:
                return 'X'
            if values == ['O', 'O', 'O']:
                return 'O'
        if '' not in board:
            return 'tie'
        return None

    def lock_buttons(self):
        """
        Disables all buttons on the board (used when the AI is thinking).
        """

        for button in self.buttons:
            button.config(state='disabled')

    def unlock_buttons(self):
        """
        Enables all buttons on the board (used after the AI makes a move).
        """
        for button in self.buttons:
            button.config(state='normal')

class MainMenu:
    """
    The main menu of the game, from where you can choose to start a game against another player or against the AI.
    """

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe - Main Menu')

        self.window.configure(background='white')

        self.label = tk.Label(self.window, text="Select game mode", font=('Helvetica', '20'), bg='white')
        self.label.pack(pady=10)

        self.two_players_button = tk.Button(self.window, text="2 Players", command=self.start_two_players_game, 
                                            font=('Helvetica', '20'), bg='sky blue', activebackground='deep sky blue')
        self.two_players_button.pack(fill='both', padx=20, pady=10)
        self.easy_ai_button = tk.Button(self.window, text="Easy AI", command=self.start_easy_ai_game, 
                                        font=('Helvetica', '20'), bg='sky blue', activebackground='deep sky blue')
        self.easy_ai_button.pack(fill='both', padx=20, pady=10)
        self.hard_ai_button = tk.Button(self.window, text="Hard AI", command=self.start_hard_ai_game, 
                                        font=('Helvetica', '20'), bg='sky blue', activebackground='deep sky blue')
        self.hard_ai_button.pack(fill='both', padx=20, pady=10)

        self.window.mainloop()

    def start_two_players_game(self):
        """
        Starts a new game with two human players.
        """

        self.window.destroy()
        TicTacToe()

    def start_easy_ai_game(self):
        """
        Starts a new game against the AI in easy mode.
        """

        self.window.destroy()
        TicTacToe(ai_difficulty='easy')

    def start_hard_ai_game(self):
        """
        Starts a new game against the AI in hard mode.
        """

        self.window.destroy()
        TicTacToe(ai_difficulty='hard')

if __name__ == "__main__":
    MainMenu()