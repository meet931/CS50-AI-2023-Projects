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
    # Initialize count for counting X and O
    countX = 0
    countO = 0

    # Count how many X and O there are in the board
    countX = sum(row.count(X) for row in board)
    countO = sum(row.count(O) for row in board)

    # If there are more X then O, next turn is O
    if countX > countO:
        return O
    # If there is O == X, next turn is X
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Create a empty set of all possible actions
    allPassibleActions = set()

    # Possible moves are any cells on the board that do not already have an X or an O in them.
    # Possible moves are any cells that are EMPTY
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                allPassibleActions.add((row, col))
    
    # Return the set
    return allPassibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action")

    # The returned board state should be the board that would result from taking the original input board, 
    # and letting the player whose turn it is make their move at the cell indicated by the input action.
    row, col = action
    # You’ll likely want to make a deep copy of the board first before making any changes.
    """A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original"""
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy


# One can win the game with three of their moves in a row horizontally.
def checkRow(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False


# One can win the game with three of their moves in a row vertically.
def checkCol(board, player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False


# One can win the game with three of their moves in a row diagonally.
def checkFirstDig(board, player):
    count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][col] == player:
                count += 1
    if count == 3:
        return True
    else:
        return False

def checkSecondDig(board, player):
    count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][len(board) - row - 1] == player:
                count += 1
    if count == 3:
        return True
    else: 
        return False

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # If the X player has won the game, your function should return X. 
    if checkRow(board, X) or checkCol(board, X) or checkFirstDig(board, X) or checkSecondDig(board, X):
        return X

    # If the O player has won the game, your function should return O.
    elif checkRow(board, O) or checkCol(board, O) or checkFirstDig(board, O) or checkSecondDig(board, O):
        return O

    # If there is no winner of the game (either because the game is in progress, or because it ended in a tie), 
    # the function should return None.
    else:
        return None


def terminal(board):
    """
    Returns True if game is over or someone has won the game or because all cells have been filled without 
    anyone winning, False otherwise.
    """
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True

    # return False if the game is still in progress (there are cells EMPTY).
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                return False

    # For the case if there was a tie
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


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Case of player is X
    elif player(board) == X:
        plays = []

        # Loop over the action to get the max value for X and min value for O
        for action in actions(board):
            
            # Add in plays a tupple with the min_value and the action that results to its value
            plays.append([min_value(result(board, action)), action])

        # Reverse sort for the plays list and get the action that should take
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]

    # Case of player is O
    elif player(board) == O:
        plays = []
        
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0])[0][1]