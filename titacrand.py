import numpy as np
import random
import time
#import matplotlib as mtp

#TODO: Optimize state search
#TODO: Implement matplotlib graphing to show results graphicaly
#TODO: Sort into class functions
#TODO: Optimize stuff


def state(board):
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
    if all(i==1 for i in board[:,1]) or all(i==2 for i in board[:,1]):
        return True,col
    if all(i==1 for i in board[:,1]) or all(i==2 for i in board[:,1]):
        return True,col
    if all((i==1)for i in board[0]) or all((i==2) for i in board[0]):
        return True,row
    if all((i==1)for i in board[1]) or all((i==2) for i in board[1]):
        return True,row
    if all((i==1)for i in board[2]) or all((i==2) for i in board[2]):
        return True,row
    return False, diag

def game(board, itrs):
   # weight = 0
   # stats = [0,0,0,0,0,0]
    cur_state = state(board)[0]
    p1wins = 0
    p2wins = 0
    diagwins = 0
    colwins = 0
    rowwins = 0
    draws = 0
    valp1 = 1
    valp2 = 2
    
    for _ in range(itrs):

        pos = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        while not cur_state and len(pos) > 0:

            cordp1 = random.choice(pos)
            board[cordp1[0], cordp1[1]] = valp1
            pos.remove(cordp1)
            print("Coordinate played by p1: {}".format(cordp1))
            print(board)
            print("Remaining moves: {}".format(pos))
            cur_state = state(board)[0]
            if cur_state == True:
                break


            if len(pos) == 0:
                break
            cordp2 = random.choice(pos)
            board[cordp2[0], cordp2[1]] = valp2
            pos.remove(cordp2)
            print("Coordinate played by p2: {}".format(cordp2))
            print(board)
            print("Remaining moves: {}".format(pos))
            cur_state = state(board)[0]
            if cur_state == True:
                break
            
        if cur_state == True:
            #if there is a multiple of two moves availbel in pos, player 1 has won
            if len(pos) % 2 == 0: 
                p1wins += 1
                print("Player 1 Wins")
            else:
            #else player 2 wins
                p2wins += 1
                print("Player 2 Wins")
                
            if state(board)[1] == 0:
                colwins += 1
                print("Game Won by Column")
                
            elif state(board)[1] == 1:
                rowwins+=1
                print("Game Won by Row")
            else:
                diagwins+=1
                print("Game Won by Diagonal")
        else:
            draws += 1
            print("Game Draw")

        pos = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        cur_state = False
        board = np.zeros((3,3), dtype=int)
        
    

    #pos = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]

    #print(used)0
    '''stats[0] = p1wins
    stats[1] = p2wins
    stats[2] = colwins
    stats[3] = rowwins
    stats[4] = diagwins
    stats[5] = draws
    stats[6] = total_games'''
    return [p1wins, p2wins, colwins, rowwins, diagwins, draws, itrs]

if __name__ == "__main__":
    #pos =  [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
    main_stats = [0,0,0,0,0,0]
    brd = np.zeros((3,3), dtype=int)
    itrs = 1000
    begin = time.time()
    stats = game(brd, itrs)
    
    #check
    check = (f"{stats[0] + stats[1] + stats[5]} =?= {itrs}")

    first_chance_win = (stats[0]/itrs)*100
    sec_chance_win = (stats[1]/itrs)*100
    drw_chance_win = (stats[5]/itrs)*100

    print(check)
    print(stats)
    print("P1 Win Percentage: {}%".format(round(first_chance_win)))
    print("P2 Win Percentage: {}%".format(round(sec_chance_win)))
    print("Draw Percentage {}%".format(round(drw_chance_win)))
    end = time.time()
    print("Time Taken: {}".format(end-begin))
