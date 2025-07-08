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
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == X:
                x_amount += 1
            elif board[i][j] == O:
                o_amount += 1
    
    # if there are the same amount of X's and O's
    # it is the X Player's turn, otherwise, it is the O Player's turn
    if x_amount == o_amount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # creates a list of actions
    possible_actions = []

    # adds the coordinates of each empty cell to the list of possible actions
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                possible_actions.append((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # creates a deep copy of the passed in board state
    new_board = copy.deepcopy(board)

    # if there is no move, a copy of the same board is returned
    if action == None:
        return new_board
    # raises an exception if the move is invalid
    elif board[action[0]][action[1]] != EMPTY:
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

    for i in range(0, 3):
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
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                return False

    # the game is over if there are no empty cells left
    return True
            

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game is over there is no move to be returned
    if terminal(board) == True:
        return None
    else:
        # if it's X's turn, return the score and move that is most optimal
        if player(board) == X:
            value, move = max_value(board)
            return move
        # if it's O's turn, return the score and move that is most optimal
        elif player(board) == O:
            value, move = min_value(board)
            return move


def max_value(board):
    
    # if the game is over, return the utility of the board
    if terminal(board) == True:
        return utility(board), None
    
    # initialize v to below min possible score
    v = -2
    move = None

    # for each possible action in the current board state
    for action in actions(board):
        
        # get the score for each action possible
        score, action = min_value(result(board, action))
        # if the score is better (higher) than the current best score, store the move for later
        if score > v:
            v = score
            move = action
            # if the best possible score is achieved, break the loop and return early
            # this is alpha-beta pruning
            if score == 1:
                return v, move

    return v, move


def min_value(board):

    # if the game is over, return the utility of the board and no move
    if terminal(board) == True:
        return utility(board), None
    
    # initialize v to above max possible score
    v = 2
    move = None

    # for each action possible for the board state
    for action in actions(board):
        
        # get the score for each action
        score, action = max_value(result(board, action))
        # if the score is better (lower) than previous best score, store the move
        if score < v:
            v = score
            move = action
            # if the best possible score is achieved, break the loop and return early
            # this is alpha-beta pruning
            if score == -1:
                return v, move
            
    return v, move
