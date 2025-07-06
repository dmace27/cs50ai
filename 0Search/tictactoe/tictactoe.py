"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_amount = 0
    o_amount = 0

    # counts how many X's and O's are on the board 
    for i in board:
        for j in board[i]:
            if board[i][j] == "X":
                x_amount += 1
            elif board[i][j] == "O":
                o_amount += 1
    
    # if there are the same amount of X's and O's
    # it is the X Player's turn, otherwise, it is the O Player's turn
    if x_amount == o_amount:
        return "X"
    else:
        return "O"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # creates a list of actions
    possible_actions = []

    # adds the coordinates of each empty cell to the list of possible actions
    for i in board:
        for j in board[i]:
            if board[i][j] == "EMPTY":
                possible_actions.append((i, j))

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # creates a deep copy of the passed in board state
    new_board = copy.deepcopy(board)

    # raises an exception if the move is invalid
    if board[action[0]][action[1]] != "EMPTY":
        raise Exception
    # returns a new board state
    else:
        new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 8 different ways to win for either player
    # if one of those conditons is not met then return None

    for i in board:
        # checks if any player won horizontally
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        
        # checks if any player won vertically
        elif board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
        
        # checks if any player won on either diagonol
        elif board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        elif board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        # if no player won
        else:
            return None
        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there is a winner, the game is over
    if winner(board) != None:
        return True
    
    # if there is no winner and there are empty cells,
    # the game is not over
    for i in board:
        for j in board[i]:
            if board[i][j] == "EMPTY":
                return False

    # the game is over if there are no empty cells left
    return True
            

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
