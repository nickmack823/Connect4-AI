class Board:

    def __init__(self, move_history=None):
        self.board_history = []
        self.move_history = []
        self.board = [0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0]
        self.true_board = []
        self.game_over = False
        # Default turn to be player 1
        self.turn = 1
        self.winner = None
        # win_path for printing out winning connection
        self.win_path = []
        self.recent_move = (0,0)
        self.connected_pieces = [0, 0]
        if move_history is not None:
            for move in move_history:
                self.makeMove(move)

    'Move can be 0-6, with the value representing which column (0-6) to place a piece in.'
    def isValidMove(self, move):
        if move in self.getPossibleMoves():
            return True
        else:
            return False

    'Returns a list of valid moves based on current board state'
    def getPossibleMoves(self):
        possible_moves = []
        for move in range(0,7):
            # Check if top item in column is empty
            if self.board[move] == 0:
                possible_moves.append(move)
        return possible_moves

    'Makes move based on input move variable (move variable represents which column to drop piece in, from 0-6)'
    def makeMove(self, move):
        self.move_history.append(move)
        # Apparently minimax and a-b don't work if you use self.board instead of self.board[:]...apparently the '[:]'
        # makes a copy of the board with altering the original (according to Google)? idk
        self.board_history.append(self.board[:])
        player = self.turn
        row = self.getMoveRow(move)
        space = 7*row + move
        self.board[space] = player
        column = move
        move_position = (row, column)
        self.recent_move = move_position
        win = self.checkForWin(move_position)
        if win:
            self.game_over = True
            self.winner = player
        # If top row is full and no winner, draw
        if 0 not in self.board[0:7]:
            self.game_over = True
            self.winner = 0
        self.turn = abs(self.turn - 3)

    'Gets the row at which a piece inserted into the given column will fall.'
    def getMoveRow(self, move):
        column = move
        # Check column for first empty space (reverse range to start at bottom of board)
        for row in reversed(range(0,6)):
            current_space = self.board[(7*row + column)]
            if current_space == 0:
                return row

    'Checks if the space at move_position is involved in a Connect4 winning sequence'
    def checkForWin(self, move_position):
        connect4 = self.checkAdjacentSpaces(move_position)
        return connect4

    ' Gets a space in the board by row and column input (returns None if space off board)'
    def getSpace(self, row, column):
        if row < 0 or row > 5 or column < 0 or column > 6:
            return None
        return self.board[7*row + column]

    ' Checks spaces adjacent to given position'
    def checkAdjacentSpaces(self, move_position):
        # Note: self.turn will either be 1 or 2, with 1 therefore representing a piece by player 1 and 2
        # representing a piece by player 2
        # Checks left and/or right of move until out of bounds, piece by other player found, or Connect4 found.

        connected = 1
        self.win_path = [(7*move_position[0]) + move_position[1]]
        for n in range(1, 4):
            # Checks right of space if spaces are available on the right
            if move_position[1] + n <= 6:
                if self.getSpace(move_position[0], move_position[1] + n) != self.turn:
                    break
                connected += 1
                self.win_path.append((7 * move_position[0]) + move_position[1] + n)
            if connected == 4:
                return True
        for n in range(1, 4):
            # Checks left of space if spaces are available on the left
            if move_position[1] - n >= 0:
                if self.getSpace(move_position[0], move_position[1] - n) != self.turn:
                    break
                connected += 1
                self.win_path.append((7 * move_position[0]) + move_position[1] - n)
            if connected == 4:
                return True

        # Checks for Connect4 in downwards direction direction (if possible to obtain)
        connected = 1
        self.win_path = [(7*move_position[0]) + move_position[1]]
        for n in range(1, 4):
            # If piece below is not this player's piece
            if self.getSpace(move_position[0] + n, move_position[1]) != self.turn:
                break
            connected += 1
            self.win_path.append((7 * (move_position[0] + n)) + move_position[1])
            # Loop checked all 3 pieces below and didn't break, so Connect4 achieved
            if connected == 4:
                return True

        # Checks for Connect4 in diagonal directions
        # First check left diagonal path (upper left to lower right)
        connected = 1
        self.win_path = [(7*move_position[0]) + move_position[1]]
        for n in range(1, 4):
            if self.getSpace(move_position[0] - n, move_position[1] - n) != self.turn:
                break
            connected += 1
            self.win_path.append((7 * (move_position[0] - n)) + move_position[1] - n)
            if connected == 4:
                return True
            # Check diagonal spaces in the lower right
        for n in range(1, 4):
            if self.getSpace(move_position[0] + n, move_position[1] + n) != self.turn:
                break
            connected += 1
            self.win_path.append((7 * (move_position[0] + n)) + move_position[1] + n)
            if connected == 4:
                return True

        # Now check lower left diagonal
        # Resets connected count after checking left diagonal path, now checks right diagonal path
        connected = 1
        self.win_path = [(7*move_position[0]) + move_position[1]]
        for n in range(1, 4):
            if self.getSpace(move_position[0] - n, move_position[1] + n) != self.turn:
                break
            connected += 1
            self.win_path.append((7 * (move_position[0] - n)) + move_position[1] + n)
            if connected == 4:
                return True
        for n in range(1, 4):
            if self.getSpace(move_position[0] + n, move_position[1] - n) != self.turn:
                break
            connected += 1
            self.win_path.append((7 * (move_position[0] + n)) + move_position[1] - n)
            if connected == 4:
                return True

        self.win_path = []
        return False
    def checkAdjacentSpacesHeuristic(self, move_position):
        # Note: self.turn will either be 1 or 2, with 1 therefore representing a piece by player 1 and 2
        # representing a piece by player 2
        # Checks left and/or right of move until out of bounds, piece by other player found, or Connect4 found.
        max_connected = 1
        connected = 1
        for n in range(1, 4):
            # Checks right of space if spaces are available on the right
            if move_position[1] + n <= 6:
                if self.getSpace(move_position[0], move_position[1] + n) != self.turn:
                    break
                connected += 1
            if connected > max_connected:
                max_connected = connected
        for n in range(1, 4):
            # Checks left of space if spaces are available on the left
            if move_position[1] - n >= 0:
                if self.getSpace(move_position[0], move_position[1] - n) != self.turn:
                    break
                connected += 1
            if connected > max_connected:
                max_connected = connected
        # Checks for Connect4 in downwards direction direction (if possible to obtain)
        connected = 1
        for n in range(1, 4):
            # If piece below is not this player's piece
            if self.getSpace(move_position[0] + n, move_position[1]) != self.turn:
                break
            connected += 1
            # Loop checked all 3 pieces below and didn't break, so Connect4 achieved
            if connected > max_connected:
                max_connected = connected

        # Checks for Connect4 in diagonal directions
        # First check left diagonal path (upper left to lower right)
        connected = 1
        for n in range(1, 4):
            if self.getSpace(move_position[0] - n, move_position[1] - n) != self.turn:
                break
            connected += 1

            if connected > max_connected:
                max_connected = connected
            # Check diagonal spaces in the lower right
        for n in range(1, 4):
            if self.getSpace(move_position[0] + n, move_position[1] + n) != self.turn:
                break
            connected += 1
            
            if connected > max_connected:
                max_connected = connected

        # Now check lower left diagonal
        # Resets connected count after checking left diagonal path, now checks right diagonal path
        connected = 1
        for n in range(1, 4):
            if self.getSpace(move_position[0] - n, move_position[1] + n) != self.turn:
                break
            connected += 1
            if connected > max_connected:
                max_connected = connected
        for n in range(1, 4):
            if self.getSpace(move_position[0] + n, move_position[1] - n) != self.turn:
                break
            connected += 1
            if connected > max_connected:
                max_connected = connected

        return max_connected
    def checkAdjacentSpacesHeuristicEnemy(self, move_position):
        # Note: self.turn will either be 1 or 2, with 1 therefore representing a piece by player 1 and 2
        # representing a piece by player 2
        # Checks left and/or right of move until out of bounds, piece by other player found, or Connect4 found.
        max_connected = 1
        connected = 1
        for n in range(1, 4):
            # Checks right of space if spaces are available on the right
            if move_position[1] + n <= 6:
                if self.getSpace(move_position[0], move_position[1] + n) == self.turn:
                    break
                connected += 1
            if connected > max_connected:
                max_connected = connected
        for n in range(1, 4):
            # Checks left of space if spaces are available on the left
            if move_position[1] - n >= 0:
                if self.getSpace(move_position[0], move_position[1] - n) == self.turn:
                    break
                connected += 1
            if connected > max_connected:
                max_connected = connected
        # Checks for Connect4 in downwards direction direction (if possible to obtain)
        connected = 1
        for n in range(1, 4):
            # If piece below is not this player's piece
            if self.getSpace(move_position[0] + n, move_position[1]) == self.turn:
                break
            connected += 1
            # Loop checked all 3 pieces below and didn't break, so Connect4 achieved
            if connected > max_connected:
                max_connected = connected

        # Checks for Connect4 in diagonal directions
        # First check left diagonal path (upper left to lower right)
        connected = 1
        for n in range(1, 4):
            if self.getSpace(move_position[0] - n, move_position[1] - n) == self.turn:
                break
            connected += 1
            if connected > max_connected:
                max_connected = connected
            # Check diagonal spaces in the lower right
        for n in range(1, 4):
            if self.getSpace(move_position[0] + n, move_position[1] + n) == self.turn:
                break
            connected += 1
            if connected > max_connected:
                max_connected = connected

        # Now check lower left diagonal
        # Resets connected count after checking left diagonal path, now checks right diagonal path
        connected = 1
        for n in range(1, 4):
            if self.getSpace(move_position[0] - n, move_position[1] + n) == self.turn:
                break
            connected += 1
            if connected > max_connected:
                max_connected = connected
        for n in range(1, 4):
            if self.getSpace(move_position[0] + n, move_position[1] - n) == self.turn:
                break
            connected += 1
            if connected > max_connected:
                max_connected = connected

        return max_connected

    'Undoes previous move'
    def undoMove(self):
        # Replace board with most recent board
        self.board = self.board_history.pop()
        # Remove previous move from move history
        self.move_history.pop()
        self.game_over = False
        self.winner = None
        self.turn = abs(self.turn - 3)

    'Prints out a representation of the board to the console'
    def printBoard(self):
        i = 0
        recentRow = self.recent_move[0]
        recentColumn = self.recent_move[1]
        recentIndex = recentRow*7 + recentColumn
        while i < len(self.board):
            if self.winner != None:
                if (i in self.win_path):
                    print(" " + "\x1b[7;32;40m" + str(self.board[i]) + "\x1b[0m" +" ", end='')
                else:
                    # end='' prevents new line
                    print(" " + str(self.board[i]) + " ", end='')
            elif i == recentIndex:
                if self.turn == 1:
                    print(" " + "\x1b[1;31;40m" + str(self.board[i]) + "\x1b[0m" +" ", end='')
                else:
                    print(" " + "\x1b[1;34;40m" + str(self.board[i]) + "\x1b[0m" + " ", end='')
            else:
                print(" " + str(self.board[i]) + " ", end='')
            # When end of row reached
            if (i + 1) % 7 == 0:
                print("")
            i = i + 1
