import random, math

PLAYER_PIECE = 1
AI_PIECE = 2
MAX_COLUMN_HEIGHT = 6 
COLUMNUM = 7


#----------- Utility and helper functions -----------

# Printing function for the 2D Board Array
def printBoard(board):
    for row in range(MAX_COLUMN_HEIGHT):
        row_array = []
        for col in range(COLUMNUM):
            row_array.append(board[col][row])
        print(row_array)

# Get list of columns that are not full
def getValidColumns(board):
    eligible = []
    for column in range(COLUMNUM):
        if board[column][0] == 0:
             eligible.append(column)
    return eligible

# Get the lowest row number (largest index) that a piece can be dropped at
def lowestFreeRow(board, column):
     for row in range(MAX_COLUMN_HEIGHT - 1, -1, -1):
            if board[column][row] == 0:
                return row

# Find 4 in a row    
def checkGameOver(board):

    # Vertical Scan
    for stack in board:
        inARow = 0
        for i in range(MAX_COLUMN_HEIGHT - 1):
            if stack[i] == stack[i+1] and stack[i] != 0:
                inARow += 1
            else: 
                inARow = 0

            if inARow >= 3:
                return stack[i]

    # Horizontal Scan
    for row in range(MAX_COLUMN_HEIGHT):
        inARow = 0
        for column in range(COLUMNUM - 1):
            if board[column][row] == board[column + 1][row] and board[column][row] != 0:
                inARow += 1
            else:
                inARow = 0
            if inARow >= 3:
                return board[column][row]
            
    # Positive diagonal wins
    for cindex in range(COLUMNUM - 3):
        for rindex in range(MAX_COLUMN_HEIGHT - 3):
            piece = board[cindex][rindex]
            if piece != 0 and board[cindex + 1][rindex + 1] == piece and board[cindex + 2][rindex + 2] == piece and board[cindex + 3][rindex + 3] == piece:
                return piece

    # Negative diagonal wins
    for cindex in range(COLUMNUM - 3):
        for rindex in range(3, MAX_COLUMN_HEIGHT):
            piece = board[cindex][rindex]
            if piece != 0 and board[cindex + 1][rindex - 1] == piece and board[cindex + 2][rindex - 2] == piece and board[cindex + 3][rindex - 3] == piece:
                return piece
    return 0

#----------- Heuristic and Algorithm functions ----------
            
# Analyse each horizontal, vertical, and diagonal section of the new state 
# in windows of 4
def windowAnalysis(window, player):
    score = 0
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2
    # Stop opponent win if they obtain 3 in a row in a window
    if window.count(PLAYER_PIECE) == 3 and window.count(0) == 1:
        score -= 4
    return score

# Heuristic for board state, retrieve horizontal, vertical, and diagonal windows of 4
# for easy scoring. 
def stateAnalysis(board, player):
    stateScore = 0

    # Preference towards center column due to inherent value of the position
    centerCol = board[COLUMNUM//2]
    centerCount = centerCol.count(player)
    stateScore += centerCount * 3
    
    # Horizontal heuristic - count the number of pieces in any given horizontal window of length 4 
    
    for row in range(MAX_COLUMN_HEIGHT):
        row_array = []
        # Step 1: Obtain one row from the board
        for col in range(COLUMNUM):
            row_array.append(board[col][row])
        # Step 2: Take 4-length list splices out of the row for analysis
        for column in range(COLUMNUM - 3):
            window = row_array[column:column + 4]
            # Counting occurs in windowAnalysis
            stateScore += windowAnalysis(window, player)

    # Vertical windows 
    for col in range(COLUMNUM):
        col_array = []
        for row in range(MAX_COLUMN_HEIGHT):
            col_array.append(board[col][row])
        for row in range(MAX_COLUMN_HEIGHT - 3):
            window = col_array[row:row + 4]
            stateScore += windowAnalysis(window, player)
        
    # Positive diagonals
    for row in range(MAX_COLUMN_HEIGHT - 3):
        for col in range(COLUMNUM - 3):
            window = [board[col + i][row + i] for i in range(4)]
            stateScore += windowAnalysis(window, player)
   
    # Negative diagonals
    for row in range(MAX_COLUMN_HEIGHT - 3):
        for col in range(COLUMNUM - 3): 
            window = [board[col + i][row + 3 - i] for i in range(4)]
            stateScore += windowAnalysis(window, player)

    return stateScore

# Minimax Algorithm
def minimax(board, depth, alpha, beta, maximizing):
    # Game End and terminal node checks
    if depth == 0 or checkGameOver(board) == 1 or checkGameOver(board) == 2 or len(getValidColumns(board)) == 0:
        if checkGameOver(board) == 1:
            return (None, -100000)
        elif checkGameOver(board) == 2:
            return (None, 100000)
        elif depth ==  0:
            return (None, stateAnalysis(board, AI_PIECE))
        else:
            return (None, 0)
    moveset = getValidColumns(board)

    if maximizing:
        value = -math.inf 
        bestCol = random.choice(moveset)
        for column in moveset: 
            row = lowestFreeRow(board, column)
            clone = [row[:] for row in board]
            clone[column][row] = AI_PIECE
            newScore = minimax(clone, depth - 1, alpha, beta, False)[1]

            if newScore > value: 
                value = newScore
                bestCol = column

            # Alpha-beta pruning
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (bestCol, value)

    else:
        value = math.inf
        bestCol = random.choice(moveset)
        for column in moveset: 
            row = lowestFreeRow(board, column)
            clone = [row[:] for row in board]
            clone[column][row] = PLAYER_PIECE
            newScore = minimax(clone, depth - 1, alpha, beta, True)[1]

            if newScore < value: 
                value = newScore
                bestCol = column
                
            # Alpha-beta pruning
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (bestCol, value)

# Main game loop
def main():
    gameOver = False
    board = [[0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]]

    currenTurn = PLAYER_PIECE

    while not gameOver:
        
        print("\n")
        printBoard(board)
        print("\n")
        
        # Player Input
        validChoice = False
        while not validChoice:
            try:
                playerChoice = int(input("Player 1's Turn. Please pick a column 1-7: ")) - 1
            except ValueError: 
                print("Please enter an integer 1-7. ")
            else: 
                if playerChoice < 0 or playerChoice > 6:
                    print("Please enter an integer 1-7.")
                elif playerChoice not in getValidColumns(board):
                    print("That column is full. ")
                else:
                    validChoice = True
        
        playeRow = lowestFreeRow(board, playerChoice)
        board[playerChoice][playeRow] = PLAYER_PIECE

        print("\n")
        printBoard(board)
        print("\n")

        if checkGameOver(board) == PLAYER_PIECE:
            print("Player 1 Wins. ")
            gameOver = True
    
        # Minimax call. Specify the depth of tree that the algorithm will look at.
        # This is how many moves ahead it looks. 5+ takes more increasingly more time.
    
        aiChoice, score = minimax(board, 3, -math.inf, math.inf, True)

        if aiChoice in getValidColumns(board):
            aiRow = lowestFreeRow(board, aiChoice)
            board[aiChoice][aiRow] = AI_PIECE
            print("Your opponent picked column " + str(aiChoice + 1) + ". ")

        
        if checkGameOver(board) == AI_PIECE:
            print("\n")
            printBoard(board)
            print("\n")
            
            print("Player 2 Wins. ")
            gameOver = True

if __name__ == "__main__":
    main()