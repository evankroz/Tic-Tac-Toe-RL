from pickle import dump, load
from ttrand import checkState
import numpy as np
import matplotlib as mpt
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
                    actions.apend((i,j))
        return actions
    
    def make_move(self, position, player):
        if self.board[position] != 0 or self.game_over:
            return False, self.get_state(), 0, self.game_over

    def check_win(self): 
        #from ttrand.py
        return checkState(self.board)
    
    def render(self):
        syms = {0: " ", 1: "X", -1: "O"}
        print("-------")
        for i in range(3):
            row = "|"
            for j in range(3):
                row += syms[self.bord[i,j]] + "|"
            print(row)
            print("-------")


#with the help of claude :)
class QLearn():
    def __init__(self, epsilon = 0.1, alpha = 0.5, gamma = 0.9):
        self.q_vals = {}
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
            dump(self.q_vals, f)
    
    def load_policy(self, filename):
        try:
            with open(filename, "rb") as f:
                self.q_values = load(f)
            print(f"Policy loaded from {filename}")
        except:
            print("Could not load policy from {filename}")


def train(episodes):
    env = Play()
    x = QLearn(epsiolon=0.3)
    y = QLearn(epsilon=0.3 )

    win_hist = []
    win_rate_x = []
    win_rate_o = []
    draw_rate = []

    wins_x = 0
    wins_o = 0
    draws = 0

    #implement training algo

def human_v_agent():
    #implement human vs trained agent gameplay
    pass

def plot(win_rate_x, win_rate_o, draw_rate):
    #implement visuals
    pass

if __name__ == "__main__":
    print("1. Train the agents")
    print("2. Play aainst trained agent")
    c = input("Enter your choice:")
    
    if c == "1":
        train(episodes=10000)
        print("Training Complete")
    elif c == "2":
        human_v_agent()
    else:
        print("Exiting.")
        exit()

    #print(play)