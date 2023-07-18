import tkinter as tk
from tkinter import messagebox
from random import choice
import copy

class TicTacToe:
    def __init__(self, ai_difficulty=None):
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')
        self.board = ['' for _ in range(9)]
        self.buttons = [tk.Button(self.window, width=20, height=10, command=lambda i=i : self.on_click(i)) for i in range(9)]
        self.current_player = 'X'
        self.ai_difficulty = ai_difficulty

        for i in range(3):
            for j in range(3):
                self.buttons[i * 3 + j].grid(row=i, column=j)

        if ai_difficulty and self.ai_difficulty == 'O':
            self.window.after(1000, self.ai_move)

        self.window.mainloop()

    def on_click(self, cell):
        if self.board[cell] == '' and not self.check_win():
            self.board[cell] = self.current_player
            self.buttons[cell].config(text=self.current_player)
            win = self.check_win()
            if win:
                messagebox.showinfo("Game Over", f"{win} wins!")
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O' and self.ai_difficulty:
                    self.window.after(1000, self.ai_move)

    def check_win(self):
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
        if self.ai_difficulty == 'easy':
            empty_cells = [i for i, x in enumerate(self.board) if x == '']
            if empty_cells:
                self.on_click(choice(empty_cells))
        else:
            # hard AI logic
            if len(self.available_moves(self.board)) == 9:
                square = choice(self.available_moves(self.board))
            else:
                _, square = self.minimax(copy.deepcopy(self.board), 'O')
            self.on_click(square)

    def available_moves(self, board):
        return [i for i, x in enumerate(board) if x == '']

    def minimax(self, board, player):
        available_moves = self.available_moves(board)

        if self.check_win_in_board(board) == 'X':
            return -1, None
        elif self.check_win_in_board(board) == 'O':
            return 1, None
        elif not available_moves:  # the game has ended with no winner
            return 0, None

        best_score = -float('inf') if player == 'O' else float('inf')
        best_move = None

        for move in available_moves:
            board[move] = player  # try this move for the current player
            score, _ = self.minimax(copy.deepcopy(board), 'X' if player == 'O' else 'O')

            board[move] = ''  # undo the move
            if player == 'O':  # the AI is trying to maximize its score
                if score > best_score:
                    best_score, best_move = score, move
            else:  # the human player is trying to minimize its score
                if score < best_score:
                    best_score, best_move = score, move

        return best_score, best_move

    def check_win_in_board(self, board):
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

class MainMenu:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe - Main Menu')
        self.label = tk.Label(self.window, text="Select game mode")
        self.label.pack()
        self.two_players_button = tk.Button(self.window, text="2 Players", command=self.start_two_players_game)
        self.two_players_button.pack()
        self.easy_ai_button = tk.Button(self.window, text="Easy AI", command=self.start_easy_ai_game)
        self.easy_ai_button.pack()
        self.hard_ai_button = tk.Button(self.window, text="Hard AI", command=self.start_hard_ai_game)
        self.hard_ai_button.pack()
        self.window.mainloop()

    def start_two_players_game(self):
        self.window.destroy()
        TicTacToe()

    def start_easy_ai_game(self):
        self.window.destroy()
        TicTacToe(ai_difficulty='easy')

    def start_hard_ai_game(self):
        self.window.destroy()
        TicTacToe(ai_difficulty='hard')

if __name__ == "__main__":
    MainMenu()