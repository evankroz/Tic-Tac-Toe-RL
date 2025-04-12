from pickle import dump, load
#from ttrand import checkState
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

'''
TODO: Finish writing agent training part
TODO: Write to plot
'''

#refactored tic tac toe
class Play():
    def __init__(self): 
        self.board = np.zeros((3,3), dtype=int)
        self.game_over = False
        self.winner = None

    def reset(self):
        self.board = np.zeros((3,3), dtype=int)
        self.game_over = False
        self.winner = None
        return self.get_state()
    
    def get_state(self):
        #board to tuple for dict keys
        #print (tuple(map(tuple, self.board)))
        return tuple(map(tuple, self.board))
    
    def get_available_actions(self):
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i,j] == 0:
                    actions.append((i,j))
        return actions
    
    def make_move(self, position, player):
        if self.board[position] != 0 or self.game_over:
            return False, self.get_state(), 0, self.game_over
        
        # Make the move
        self.board[position] = player
        
        # Check if game is over
        winner = self.check_win()
        if winner != 0:  # Someone won
            self.game_over = True
            self.winner = winner
            return True, self.get_state(), 1 if winner == player else -1, self.game_over
        
        # Check for draw - only if all positions are filled
        if np.all(self.board != 0):  # Changed condition to check if board is full
            self.game_over = True
            self.winner = 0  # Draw
            return True, self.get_state(), 0, self.game_over
        
        # Game continues
        return True, self.get_state(), 0, self.game_over

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
                row += syms[self.board[i,j]] + "|"
            print(row)
            print("-------")


#with the help of claude :)
class QLearn():
    def __init__(self, epsilon = 0.1, alpha = 0.5, gamma = 0.9):
        self.q_values = {}
        self.epsilon = epsilon
        self.alpha =alpha
        self.gamma = gamma
    
    def get_q_val(self, state, action):
        return self.q_values.get((state, action), 0.0)
    
    def choose_action(self, state, available_actions):
        if not available_actions:
            return None

        if random.random() < self.epsilon:
            return random.choice(available_actions)
        else:
            q_values = [self.get_q_val(state,action) for action in available_actions]
            max_q = max(q_values)

            best_actions = [action for action, q in zip(available_actions, q_values) if q == max_q]
            return random.choice(best_actions)
        
    def learn(self, state, action, reward, next_state, next_actions):
        old_val = self.get_q_val(state, action)
        if next_actions:
            next_max = max([self.get_q_val(next_state, next_action) for next_action in next_actions])
        else:
            next_max = 0
        
        new_val = old_val + self.alpha*(reward+self.gamma*next_max-old_val)
        self.q_values[(state,action)] = new_val

    def save_policy(self, filename):
        with open(filename, "wb") as f:
            dump(self.q_values, f)
    
    def load_policy(self, filename):
        try:
            with open(filename, "rb") as f:
                self.q_values = load(f)
            print(f"Policy loaded from {filename}")
        except:
            print(f"Could not load policy from {filename}")


def train(episodes):
    env = Play()
    x = QLearn(epsilon=0.3)
    o = QLearn(epsilon=0.3)

    win_hist = []
    win_rate_x = []
    win_rate_o = []
    draw_rate = []

    wins_x = 0
    wins_o = 0
    draws = 0
    window_size = 100

    for episode in tqdm(range(episodes)):
        state = env.reset()
        current_player = 1

        while not env.game_over:
            available_actions = env.get_available_actions()

            if current_player == 1:
                action = x.choose_action(state, available_actions)
            else:
                action = o.choose_action(state, available_actions)
            
            valid, next_state, reward, done=  env.make_move(action, current_player)

            if current_player == -1:
                reward = -reward
            
            next_available_actions = env.get_available_actions()

            if current_player == 1:
                x.learn(state, action, reward, next_state, next_available_actions)
            else:
                o.learn(state, action, -reward, next_state, next_available_actions)
            
            state = next_state
            current_player = -current_player

        if env.winner == 1:
            wins_x += 1
            win_hist.append(1)
        elif env.winner == -1:
            wins_o+=1
            win_hist.append(-1)
        else:
            draws += 1
            win_hist.append(0)

        if episode % window_size == 0 and episode > 0:
            recent_outcomes = win_hist[-window_size:]
            x_rate = recent_outcomes.count(1) / window_size
            o_rate = recent_outcomes.count(-1) / window_size
            d_rate = recent_outcomes.count(0) / window_size
            win_rate_x.append(x_rate)
            win_rate_o.append(o_rate)
            draw_rate.append(d_rate)
        
    x.save_policy("agent_x_policy.pkl")
    o.save_policy("agent_o_policy.pkl")

    plot_results(win_rate_x, win_rate_o, draw_rate, window_size)

    print(f"Player X wins: {wins_x}, Player O wins: {wins_o}, Draws: {draws}")
    return x, o


def plot_results(win_rate_x, win_rate_o, draw_rate, window_size):
    plt.figure(figsize=(10, 6))
    episodes = [i * window_size for i in range(len(win_rate_x))]
    
    plt.plot(episodes, win_rate_x, label='Player X win rate', color='blue')
    plt.plot(episodes, win_rate_o, label='Player O win rate', color='red')
    plt.plot(episodes, draw_rate, label='Draw rate', color='green')
    
    plt.xlabel('Episodes')
    plt.ylabel('Rate')
    plt.title(f'Win and Draw Rates (Moving Average over {window_size} games)')
    plt.legend()
    plt.grid(True)
    plt.savefig('tic_tac_toe_learning_progress.png')
    plt.close()
    #implement training algo

def human_vs_agent():
    """Let a human play against the trained agent"""
    env = Play()
    agent_x = QLearn(epsilon=0)  # No exploration during gameplay
    agent_x.load_policy("agent_x_policy.pkl")
    
    while True:
        state = env.reset()
        current_player = 1  # X (agent) goes first
        
        while not env.game_over:
            env.render()
            
            if current_player == 1:
                print("Agent (X) is thinking...")
                available_actions = env.get_available_actions()
                action = agent_x.choose_action(state, available_actions)
                print(f"Agent chooses position: {action[0]+1}, {action[1]+1}")
            else:
                available_actions = env.get_available_actions()
                valid_input = False
                while not valid_input:
                    try:
                        print("Available positions:", [(a[0]+1, a[1]+1) for a in available_actions])
                        row = int(input("Enter row (1-3): ")) - 1
                        col = int(input("Enter column (1-3): ")) - 1
                        action = (row, col)
                        if action in available_actions:
                            valid_input = True
                        else:
                            print("Invalid position! Try again.")
                    except ValueError:
                        print("Please enter numbers between 1 and 3.")
                        
            valid, state, reward, done = env.make_move(action, current_player)
            current_player = -current_player  # Switch players
            
        # Display final state
        env.render()
        
        if env.winner == 1:
            print("Agent (X) wins!")
        elif env.winner == -1:
            print("Human (O) wins!")
        else:
            print("It's a draw!")
            
        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            break


if __name__ == "__main__":
    print("1. Train the agents")
    print("2. Play aainst trained agent")
    c = input("Enter your choice:")
    
    if c == "1":
        train(episodes=100000)
        print("Training Complete")
    elif c == "2":
        human_vs_agent()
    else:
        print("Exiting.")
        exit()

    #print(play)