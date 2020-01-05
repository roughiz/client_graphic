'''***************************This file is containing the main function of a Four in a row AI****************************************
   ***************************we used several functions of the file fourinarow.py ****************************************
   ***************************Author : Mohammed Yacine BERREZOUG ****************************************'''
import copy

BOARDWIDTH = 5
BOARDHEIGHT = 6
INFINITY = 100000

'''Old functions'''

def isBoardFull(board):
    #this function checks if all cells are filed in the game board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == ' ':
                return False
    return True
def isValidMove(board, move):
    # this function check if the move is valid, it means,
    # if the move value is between 0 and Board width included, and if we have a free(' ' filed) entry in the player move column in the board
    if move < 0 or move >= (BOARDWIDTH):
        return False

    if board[move][0] != ' ':
        return False

    return True

def makeMove(board, player, column):
    # In a column, we check the first space filed tile(free entry) vertically from the bottom to the top, to write the player move in
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            return board  #'''Modif return board'''

def isWinner(board, tile):
    #This function checks if we have 4 successive player tile horizontally or vertically or diagonally

    # check horizontal spaces
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True

    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True

    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True

    return False

'''New functions'''

def getValidMoves(board):
    "This function return valid moves from a state of board"
    return [x for x in range(BOARDWIDTH)
            if isValidMove(board,x)]

def getSuccessors(board, tile):
    "Return a list of valid (move, state) pairs."
    return [(move, makeMove(copy.deepcopy(board), tile, move)) for move in getValidMoves(board)]
def isGameOver(board):
    "This function return true if there is a winner"
    return isWinner(board,'X') or isWinner(board,'O')

def checkFor4inaRow(board, tile):
    "This function counts the number of 4 successive player tile horizontally or vertically or diagonally"

    count=0
    # check horizontal spaces
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                count+=1

    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                count += 1

    # check / diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                count += 1

    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                count += 1

    return count


def checkFor3inaRow(board, tile):
    #This function counts the number of 3 successive player tile horizontally or vertically or diagonally

    count = 0
    # check horizontal spaces
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 2):
            if board[x][y] == tile and board[x + 1][y] == tile and board[x + 2][y] == tile:
                count += 1

    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 2):
            if board[x][y] == tile and board[x][y + 1] == tile and board[x][y + 2] == tile:
                count += 1

    # check / diagonal spaces
    for x in range(BOARDWIDTH - 2):
        for y in range(2, BOARDHEIGHT):
            if board[x][y] == tile and board[x + 1][y - 1] == tile and board[x + 2][y - 2] == tile:
                count += 1

    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 2):
        for y in range(BOARDHEIGHT - 2):
            if board[x][y] == tile and board[x + 1][y + 1] == tile and board[x + 2][y + 2] == tile:
                count += 1

    return count

def checkFor2inaRow(board, tile):
    # This function counts the number of 2 successive player tile horizontally or vertically or diagonally

    count = 0
    # check horizontal spaces
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 1):
            if board[x][y] == tile and board[x + 1][y] == tile:
                count += 1

    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 1):
            if board[x][y] == tile and board[x][y + 1] == tile:
                count += 1

    # check / diagonal spaces
    for x in range(BOARDWIDTH - 1):
        for y in range(1, BOARDHEIGHT):
            if board[x][y] == tile and board[x + 1][y - 1] == tile:
                count += 1

    # check \ diagonal spaces
    for x in range(BOARDWIDTH - 1):
        for y in range(BOARDHEIGHT - 1):
            if board[x][y] == tile and board[x + 1][y + 1] == tile:
                count += 1

    return count

def heuristicEval(board, playerTile):
    '''This function evaluates a board state and return a score which will be used on choosing best move, So,
    the heuristic used is : Score = player 4 successive tile Count*1000 + player 3 successive tile Count*100 + player 2 successive tileCount*10
    - (enemy 4 successive tile Count*1000 + enemy 3 successive tile * 100 + enemy 2 successive tile Count*10)'''

    if playerTile == 'X': #Check the player tile and take the other for the enemy
        enemyTile = 'O'
    else:
        enemyTile = 'X'

    player4inaRowCount = checkFor4inaRow(board,playerTile)
    player3inaRowCount = checkFor3inaRow(board, playerTile)
    player2inaRowCount = checkFor2inaRow(board, playerTile)

    enemy4inaRowCount = checkFor4inaRow(board, enemyTile)
    enemy3inaRowCount = checkFor3inaRow(board, enemyTile)
    enemy2inaRowCount = checkFor2inaRow(board, enemyTile)


    return player4inaRowCount*1000 + player3inaRowCount*100 + player2inaRowCount*10 - (enemy4inaRowCount*1000 + enemy3inaRowCount*100 + enemy2inaRowCount*10)

def getBestMove(board, playerTile, enemyTile, depth):
    '''This function return the best move player can do from a board state according to a depth of look ahead in the potential moves tree.
    For each state child, it calls a NegaMax algorithm with an Alpha Beta pruning, and finally return the move which have the best score'''

    scoresByMoves = {}
    for (m, s) in getSuccessors(board, playerTile):
        scoresByMoves[m] = -alphabetaSearch(s, enemyTile, playerTile, -INFINITY, +INFINITY, depth) # we are calling NegaMax AlphaBeta function on each child with alpha = -oo and beta = +oo init

    bestScore = -INFINITY
    bestMove = 0
    movesAndScores = scoresByMoves.items()
    for move, score in movesAndScores:
        #choosing the best move
        if score >= bestScore:
            bestScore=score
            bestMove=move

    return bestMove, bestScore


def alphabetaSearch(board, playerTile, enemyTile, alpha, beta, depth):
    '''This function makes it possible to evaluate the possible movements according to a NegaMax algorithm with alpha beta pruning
    , until reaching the maximum depth or a final state'''

    if isGameOver(board) or isBoardFull(board) or (depth == 0): # We check if we have a final state or if we reach the max depth
        return heuristicEval(board,playerTile)

    vmax = -INFINITY
    for (a, s) in getSuccessors(board, playerTile):
        v = -alphabetaSearch(s, enemyTile, playerTile, -beta, -alpha, depth - 1) # recursive call to our function for each child with an inversion of sign to get max on opponent player
        vmax = max(v, vmax)
        alpha = max(alpha, v)
        if alpha >= beta:
            return alpha # pruning

    return vmax