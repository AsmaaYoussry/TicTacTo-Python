#UCS
import tkinter as tk
from tkinter import messagebox
import heapq

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

class TicTacToeLogic:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = None
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        if len(self.players) == 2:
            self.current_player = self.players[0]

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player.symbol
            self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            return 'tie'

        return None

    def evaluate_board(self):
        winner = self.check_winner()
        if winner == 'tie':
            return 0
        elif winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        else:
            return 0

    def uniform_cost_search(self):
        frontier = []
        heapq.heappush(frontier, (0, [list(row) for row in self.board]))
        explored = set()

        while frontier:
            cost, current_state = heapq.heappop(frontier)

            if tuple(map(tuple, current_state)) in explored:
                continue

            explored.add(tuple(map(tuple, current_state)))

            winner = self.check_winner()
            if winner:
                if winner == 'X':
                    return 1
                elif winner == 'O':
                    return -1
                else:
                    return 0

            for row in range(3):
                for col in range(3):
                    if current_state[row][col] == ' ':
                        new_state = [list(row) for row in current_state]
                        new_state[row][col] = self.current_player.symbol
                        heapq.heappush(frontier, (cost + 1, new_state))

        return 0

    def find_best_move(self):
        best_move = None
        best_cost = float('inf')
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.current_player.symbol
                    cost = self.uniform_cost_search()
                    self.board[row][col] = ' '
                    if cost < best_cost:
                        best_cost = cost
                        best_move = (row, col)
        return best_move

class TicTacToeGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.root.title("Tic-Tac-Toe")

        for row in range(3):
            for col in range(3):
                button = tk.Button(root, text='', width=10, height=5,
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def make_move(self, row, col):
        if self.game.check_winner() is None and self.game.board[row][col] == ' ':
            self.game.make_move(row, col)
            self.update_board()

            winner = self.game.check_winner()
            if winner:
                if winner == 'tie':
                    messagebox.showinfo("Game Over", "It's a tie!")
                else:
                    messagebox.showinfo("Game Over", f"Player {winner} wins!")

                self.reset_board()
            else:
                best_move = self.game.find_best_move()
                self.game.make_move(best_move[0], best_move[1])
                self.update_board()
                winner = self.game.check_winner()
                if winner:
                    if winner == 'tie':
                        messagebox.showinfo("Game Over", "It's a tie!")
                    else:
                        messagebox.showinfo("Game Over", f"Player {winner} wins!")
                    self.reset_board()

    def update_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = self.game.board[row][col]

    def reset_board(self):
        self.game = TicTacToeLogic()
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeLogic()
    player1 = Player('X')
    player2 = Player('O')
    game.add_player(player1)
    game.add_player(player2)
    gui = TicTacToeGUI(root, game)
    root.mainloop()