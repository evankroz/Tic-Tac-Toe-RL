import numpy as np
import random
import time
import matplotlib.pyplot as plt

def checkState(board):
    col = 0
    row = 1
    diag = 2
    #make this crap faster
    if all(i==1 for i in [board[0,0], board[1,1], board[2,2]]) or all(i==2 for i in [board[0,0], board[1,1], board[2,2]]):
        return True,diag
    if all(i==1 for i in [board[2,0], board[1,1], board[0,2]]) or all(i==2 for i in [board[2,0], board[1,1], board[0,2]]):
        return True,diag
    if all(i==1 for i in board[:, 0]) or all(i==2 for i in board[:, 0]):
        return True,col
    if all(i==1 for i in board[:, 1]) or all(i==2 for i in board[:, 1]):
        return True,col
    if all(i==1 for i in board[:, 2]) or all(i==2 for i in board[:, 2]):
        return True,col
    if all((i==1)for i in board[0]) or all((i==2) for i in board[0]):
        return True,row
    if all((i==1)for i in board[1]) or all((i==2) for i in board[1]):
        return True,row
    if all((i==1)for i in board[2]) or all((i==2) for i in board[2]):
        return True,row
    return False, diag
    
class Play():
    def __init__(self, itrs, board):
        self.board = board
        self.p1 = 1
        self.p2 = 2
        self.itrs = itrs
        self.dwins = 0
        self.rwins = 0
        self.cwins = 0
        self.draws = 0
        self.p1win = 0
        self.p2win = 0
        self.cur_state = False

    def main(self):

        for _ in range(self.itrs):

            pos = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
            
            while not self.cur_state and len(pos) > 0:

                cordp1 = random.choice(pos)
                self.board[cordp1[0], cordp1[1]] = self.p1
                pos.remove(cordp1)
                print("Coordinate played by p1: {}".format(cordp1))
                print(self.board)
                print("Remaining moves: {}".format(pos))
                self.cur_state = checkState(self.board)[0]
                if self.cur_state == True:
                    break


                if len(pos) == 0:
                    break
                cordp2 = random.choice(pos)
                self.board[cordp2[0], cordp2[1]] = self.p2
                pos.remove(cordp2)
                print("Coordinate played by p2: {}".format(cordp2))
                print(self.board)
                print("Remaining moves: {}".format(pos))
                #get boolean value from state call tuple
                self.cur_state = checkState(self.board)[0]
                if self.cur_state == True:
                    break
                
            if self.cur_state == True:
                #if there is a multiple of two moves availbel in pos, player 1 has won
                if len(pos) % 2 == 0: 
                    self.p1win += 1
                    print("Player 1 Wins")
                else:
                
                #else player 2 wins
                    self.p2win += 1
                    print("Player 2 Wins")
                    
                if checkState(self.board)[1] == 0:
                    self.cwins += 1
                    print("Game Won by Column")
                elif checkState(self.board)[1] == 1:
                    self.rwins += 1
                    print("Game Won by Row")
                elif checkState(self.board)[1] == 2:
                    self.dwins+=1
                    print("Game Won by Diagonal")
            else:
                self.draws += 1
                print("Game Draw")

            pos = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
            self.cur_state = False
            self.board = np.zeros((3,3), dtype=int)
        
        #print([self.p1win, self.p2win, cwins, rwins, dwins, self.draws, itrs])
        return [self.p1win, self.p2win, self.cwins, self.rwins, self.dwins, self.draws, itrs]
    

    def graph(self):

        plt.style.use('_mpl-gallery')
        #x = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        y = [self.p1win, self.p2win, self.cwins, self.rwins, self.dwins, self.draws]
        y_names = ["P1 Wins", "P2 Wins", "Col.", "Row", "Diag.", "Draws"]

        fig, ax = plt.subplots()
        fig.set_size_inches(w = 6, h = 5)

        #p = ax.bar(x, y, width = 1, edgecolor = "white", linewidth = 0.7)
        bar_container = ax.bar(y_names, y)

        ax.set(ylim=(0, self.itrs-0.3*self.itrs))
        #ax.set_xticks(y, labels = y)
        
        plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)

        ax.bar_label(bar_container, labels = y)
        plt.ylabel("Total Iterations - 0.3*Itrs")

        #ax.legend()
        plt.title("Stats of Games where P1 plays first, P1 and P2 play random moves")
        plt.show()
        


if __name__ == "__main__":

    #base = [0,0,0,0,0,0]
    board = np.zeros((3,3), dtype = int)
    itrs = int(input("Give Num of Iterations: "))
    begin = time.time()

    play = Play(itrs,board)

    stats = play.main()

    check = (f"{stats[0] + stats[1] + stats[5]} =?= {itrs}")
    end = time.time()
    #plot = Plot(stats) 

    #plot.display()   
    first_chance_win = (stats[0]/itrs)*100
    sec_chance_win = (stats[1]/itrs)*100
    
    print(check)
    print(stats)
    print("P1 Win Percentage: {}%".format(round(first_chance_win)))
    print("P2 Win Percentage: {}%".format(round(sec_chance_win)))
    print(f"Time Taken: {end-begin}")
    play.graph()


    #statecheck = state(board)
    #print(statecheck)
