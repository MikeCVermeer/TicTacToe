import tkinter as tk
from tkinter import messagebox
from random import choice
import copy

class TicTacToe:
    def __init__(self, ai_difficulty=None):
        # Initialize the main game window
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe')

        # Set the style for the window
        self.window.configure(background='white')

        # Initialize the game board
        self.board = ['' for _ in range(9)]

        # Create buttons for the game board and link them to the "on_click" method
        self.buttons = [tk.Button(self.window, width=20, height=10, command=lambda i=i : self.on_click(i), 
                                  font=('Helvetica', '20'), bg='sky blue', activebackground='deep sky blue') for i in range(9)]

        # Start the game with player 'X'
        self.current_player = 'X'

        # Set the AI difficulty level if playing against AI
        self.ai_difficulty = ai_difficulty

        # Place the buttons on the window grid
        for i in range(3):
            for j in range(3):
                self.buttons[i * 3 + j].grid(row=i, column=j, padx=5, pady=5)

        # If AI starts, make the first move
        if ai_difficulty and self.ai_difficulty == 'O':
            self.window.after(1000, self.ai_move)
            

        self.window.mainloop()

    def on_click(self, cell):
        # Define player's action when they click a cell
        if self.board[cell] == '' and not self.check_win():
            self.board[cell] = self.current_player
            self.buttons[cell].config(text=self.current_player)
            win = self.check_win()
            if win:
                # If someone wins, display a message
                messagebox.showinfo("Game Over", f"{win} wins!")
            else:
                # If no one wins yet, change the current player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O' and self.ai_difficulty:
                    self.window.after(1000, self.ai_move)

    def check_win(self):
        # Define the win condition
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
        # Define AI's action based on difficulty level
        if self.ai_difficulty == 'easy':
            # Easy AI randomly selects an available cell
            empty_cells = [i for i, x in enumerate(self.board) if x == '']
            if empty_cells:
                self.on_click(choice(empty_cells))
        else:
            # Hard AI uses minimax algorithm to make the best move
            if len(self.available_moves(self.board)) == 9:
                square = choice(self.available_moves(self.board))
            else:
                _, square = self.minimax(copy.deepcopy(self.board), 'O')
            self.on_click(square)

    def available_moves(self, board):
        # Get all available (empty) cells in the current board
        return [i for i, x in enumerate(board) if x == '']

    def minimax(self, board, player):
        # The minimax algorithm, which is used by the hard AI to choose the best move
        available_moves = self.available_moves(board)

        # Check if the game is over
        if self.check_win_in_board(board) == 'X':
            return -1, None
        elif self.check_win_in_board(board) == 'O':
            return 1, None
        elif not available_moves:
            return 0, None

        # If the game isn't over, calculate the best score that the AI can achieve with current board status
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
        # Check if there's a winner on the given board
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
        # Initialize the main menu window
        self.window = tk.Tk()
        self.window.title('Tic Tac Toe - Main Menu')

        # Set the style for the window
        self.window.configure(background='white')

        # Add the game mode selection label
        self.label = tk.Label(self.window, text="Select game mode", font=('Helvetica', '20'), bg='white')
        self.label.pack(pady=10)

        # Add the "2 Players", "Easy AI" and "Hard AI" buttons, linked to the corresponding methods
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
        # Start a 2-player game
        self.window.destroy()
        TicTacToe()

    def start_easy_ai_game(self):
        # Start a game against an easy AI
        self.window.destroy()
        TicTacToe(ai_difficulty='easy')

    def start_hard_ai_game(self):
        # Start a game against a hard AI
        self.window.destroy()
        TicTacToe(ai_difficulty='hard')

if __name__ == "__main__":
    MainMenu()