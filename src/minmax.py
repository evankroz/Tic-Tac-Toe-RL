from random import randrange, choice
import numpy as np
import matplotlib.pyplot as plt
#from tqdm import tqdm
#import time

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.game_over = False
        self.winner = None
    
    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.game_over = False
        self.winner = None
        return self.board.copy()
    
    def get_available_positions(self):
        positions = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions
    
    def make_move(self, position, player):
        if self.board[position] != 0 or self.game_over:
            return False
        
        self.board[position] = player
        
        # Check for win or draw
        winner = self.check_win()
        if winner != 0:
            self.game_over = True
            self.winner = winner
            return True
        
        if len(self.get_available_positions()) == 0:
            self.game_over = True
            self.winner = 0  # Draw
            return True
        
        return True
    
    def check_win(self):
        # Check rows
        for i in range(3):
            if abs(np.sum(self.board[i, :])) == 3:
                return np.sign(np.sum(self.board[i, :]))
        
        # Check columns
        for i in range(3):
            if abs(np.sum(self.board[:, i])) == 3:
                return np.sign(np.sum(self.board[:, i]))
        
        # Check diagonals
        if abs(np.sum(np.diag(self.board))) == 3:
            return np.sign(np.sum(np.diag(self.board)))
        if abs(np.sum(np.diag(np.fliplr(self.board)))) == 3:
            return np.sign(np.sum(np.diag(np.fliplr(self.board))))
        
        # No winner
        return 0
    
    def render(self):
        syms = {0: " ", 1: "X", -1: "O"}
        print("-------")
        for i in range(3):
            row = "|"
            for j in range(3):
                row += syms[self.board[i, j]] + "|"
            print(row)
            print("-------")

def minimax(board, depth, is_maximizing, player, opponent):
    # Check for terminal states
    winner = check_win(board)
    if winner == player:
        return 10 - depth  # Win (prefer quicker wins)
    elif winner == opponent:
        return depth - 10  # Loss (prefer longer losses)
    elif np.all(board != 0) or depth > 9:  # Full board or max depth
        return 0  # Draw
    
    if is_maximizing:
        best_score = -float('inf')
        for i, j in [(i, j) for i in range(3) for j in range(3) if board[i, j] == 0]:
            # Make move
            board[i, j] = player
            # Recursive call
            score = minimax(board, depth + 1, False, player, opponent)
            # Undo move
            board[i, j] = 0
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i, j in [(i, j) for i in range(3) for j in range(3) if board[i, j] == 0]:
            # Make move
            board[i, j] = opponent
            # Recursive call
            score = minimax(board, depth + 1, True, player, opponent)
            # Undo move
            board[i, j] = 0
            best_score = min(score, best_score)
        return best_score

def get_best_move(board, player=1):
    """Find the best move using minimax algorithm"""
    opponent = -player
    best_score = -float('inf')
    best_move = None
    
    # Check if center is available (optimal first move)
    if board[1, 1] == 0:
        return (1, 1)
    
    # Try each available position
    for i, j in [(i, j) for i in range(3) for j in range(3) if board[i, j] == 0]:
        # Make move
        board[i, j] = player
        # Calculate score
        score = minimax(board.copy(), 0, False, player, opponent)
        # Undo move
        board[i, j] = 0
        
        if score > best_score:
            best_score = score
            best_move = (i, j)
    
    return best_move

def check_win(board):
    """Check if there's a winner on the board"""
    # Check rows
    for i in range(3):
        if abs(np.sum(board[i, :])) == 3:
            return np.sign(np.sum(board[i, :]))
    
    # Check columns
    for i in range(3):
        if abs(np.sum(board[:, i])) == 3:
            return np.sign(np.sum(board[:, i]))
    
    # Check diagonals
    if abs(np.sum(np.diag(board))) == 3:
        return np.sign(np.sum(np.diag(board)))
    if abs(np.sum(np.diag(np.fliplr(board)))) == 3:
        return np.sign(np.sum(np.diag(np.fliplr(board))))
    
    # No winner
    return 0

def human_vs_minimax():
    """Let a human play against the minimax algorithm"""
    game = TicTacToe()
    
    while True:
        board = game.reset()
        current_player = 1  # X (agent) goes first
        
        while not game.game_over:
            game.render()
            
            if current_player == 1:
                '''print("Agent (X) is thinking...")
                lst = [0.05, 0.07, 0.09, 0.11, 0.13, 0.15]
                for _  in tqdm(range(10)):
                    time.sleep(choice(lst))'''
                move = get_best_move(game.board, player=1)
                print(f"Agnet  chooses position: {move[0]+1}, {move[1]+1}")
            else:
                available_positions = game.get_available_positions()
                valid_input = False
                while not valid_input:
                    try:
                        print("Available positions:", [(p[0]+1, p[1]+1) for p in available_positions])
                        row = int(input("Enter row (1-3): ")) - 1
                        col = int(input("Enter column (1-3): ")) - 1
                        move = (row, col)
                        if move in available_positions:
                            valid_input = True
                        else:
                            print("Invalid position! Try again.")
                    except ValueError:
                        print("Please enter numbers between 1 and 3.")
            
            game.make_move(move, current_player)
            current_player = -current_player 
        
        game.render()
        
        if game.winner == 1:
            print("AI (X) wins!")
        elif game.winner == -1:
            print("Human (O) wins!")
        else:
            print("It's a draw!")
        
        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            break

def minmax_vs_minmax(num_games, show_games = False):
    game = TicTacToe()

    bot1_wins = 0
    bot2_wins = 0
    draws = 0

    for i in range(num_games):
        game.reset()
        current_player = 1

        if show_games  and i%100 == 0:
            print(f"Game {i+1}/{num_games}")

        while not game.game_over:
            if current_player == 1:
                move = get_best_move(game.board, player = 1)
            else:
                move = get_best_move(game.board, player = -1)

            game.make_move(move, current_player)

            if show_games and i<5:
                print(f"Player {current_player} places at {move}")
                game.render()
            
            current_player = -current_player

        if game.winner == 1:
            bot1_wins += 1
        elif game.winner == -1:
            bot2_wins += 1
        else:
            draws += 1

    print(f"\nResults after {num_games} games:")
    print(f"Bot 1 (X) wins: {bot1_wins} ({bot1_wins/num_games*100:.1f}%)")
    print(f"Bot 2 (O) wins: {bot2_wins} ({bot2_wins/num_games*100:.1f}%)")
    print(f"Draws: {draws} ({draws/num_games*100:.1f}%)")

    return bot1_wins, bot2_wins, draws

    
def rand_vs_minmax(num_games=100, show_games = False):
    game = TicTacToe()
    pass


if __name__ == "__main__":
    num_games = 10000
    print("Play against unbeatable Minimax AI")
    #human_vs_minimax()

    minmax_vs_minmax(num_games=num_games, show_games=True)