
import numpy as np



def calculate_board_value(starting_board,board,color):
    
    if color=="black":
        target = -1
    else:
        target = 1
    
    
    sum_now = 0
    sum_then = 0
    for x in range(8):
        for y in range(8):
            sum_now += board[y,x]*target
            sum_then += starting_board[y,x]*target
            
    return sum_now-sum_then


board1 = [
        [ -2, -3, -4, -5, -6, -4, -3, -2],
        [ -1, -1, -1, -1, -1, -1, -1, -1],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  1,  1,  1,  1,  1,  1,  1,  1],
        [  2,  3,  4,  5,  6,  4,  3,  2]]


board1 = np.array(board1)




board2 = [
        [ -2, -3, -4, -5, -6, -4, -3, -2],
        [ -1, -1, -1, -1, -1, -1, -1, -1],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  0,  0,  0,  0,  0,  0,  0,  0],
        [  1,  1,  1,  1,  1,  1,  1,  1],
        [  2,  3,  4,  5,  6,  4,  3,  2]]


board2 = np.array(board2)


print(calculate_board_value(board1,board2,"white"))