# B351-Final-Project (Connect 4 AI)

(NOTE: This program was developed as part of a group project. I worked on everything except for the methods relating to the heuristics.)

## game.py
This is the main file of our Connect4 program. Running this file allows 
the user to either run the "test suite" or to customize the game(s) that
they want to run.

    Running the program:
    1. Run game.py
    2. Input either 1 (test suite) or 2 (customized game) into the console
    3. Follow console instructions regarding further inputs
    4. Observe results

**playGame(self)**

This function is what performs the actual action of playing a Connect4
game. After initializing a starter Connect4 board, this function retrieves
and plays each move that each player decides to do and prints out the
board, ending the game only if one of the players wins after 
making their move.

**recordResult(self, result)**

This function updates the Game object's "results" dictionary, which
stores how many wins, losses, and draws there have been between the
two currently competing players.

**testSuite(self, n)**

This function plays "n" games for each possible matchup of our
algorithms (i.e. Minimax vs. Random, Minimax vs. Alpha-Beta, Minimax 
vs. Monte Carlo, Alpha-Beta vs. Random, etc.) and prints the results
using print_results.

**printResults(self, games, n)**

This function takes in a list, "games", and an integer, "n", where "games"
is a list of Game class objects that each represent a different
matchup of the test_suite, and "n" is the number of games that was played.
The results of the games are displayed along with various metrics that
measure game performance and efficiency, such as average moves considered,
time spent deciding a move, etc.

**getPlayer(cls, selection)**

This function matches a user's input when selecting a player for their
customized games(s) to a Player class type and returns a String 
denoting their selection.

**getOpponent(cls, selection)**

Exactly the same as get_player, except this function retrieves the
opponent that the user selected for their customized game(s).

## board.py

### Board

**isValidMove(self, move)**

Returns a boolean indicating whether the input "move" is a valid move
given the current board state.

**getPossibleMoves(self)**

Returns a list of all valid moves for the current board.

**makeMove(self, move)**

Makes the given move on the current board.

**getMoveRow(self, move)**

Returns the nearest empty row at which a piece of the given 
input "move" (column) will fall.

**checkForWin(self, move_position)**

Uses checkAdjacentSpaces to determine if a move at move_position
results in a win, returning a boolean that indicates if a win has been
achieved.

**getSpace(self, row, column)**

Returns the index of the board list that represents a move at the 
input "row" and "column".

**checkAdjacentSpaces(self, move_position)**

After a player has performed a move, this function is called to
determine whether the move results in a win based on its location
on the board (move_position)"

**checkAdjacentSpacesHeuristic(self, move_position)**

This function works similarly to checkAdjacentSpaces, except it returns a heuristic score for a position on the board based on how many pieces are connected at that position, instead of returning True or False for if there is a Connect Four.

**checkAdjacentSpacesHeuristicEnemy(self, move_position)**

Returns a heuristic score for a position on the board, just as checkAdjacentSpacesHeuristic does, but it checks for connected enemy pieces.

**undoMove(self)**

Undoes the most recently performed move.

**printBoard(self)**

Prints out a console representation of the current board.

## player.py

### Player

**getHeuristic(self, board)**

When called, executed and returns the value from either 
heuristic1, heuristic2, or heuristic3 based on the "heuristic" parameter
of the base Player class.

**heuristic1(self, board)**

**heuristic2(self, board)**

**heuristic3(self, board)**

### ManualPlayer(Player)

**findMove(self, move_history)**

Allows the user to manually make a move if they are playing a custom
game against the computer. Returns an integer numbered 0-6
representing the column that has been selected for the move.

### PlayerRandom(Player)

**findMove(self, move_history)**

Randomly makes a move based on the board's currently possible set of 
moves (move_history). Returns an integer numbered 0-6
representing the column that has been selected for the move.

### PlayerMM(Player)

**minimax(self, board, depth)**

Iterates through the Minimax algorithm to select a move based on the
input board and depth, using the input max_depth and heuristic parameters
to determine how far ahead and by what heuristic the algorithm
should look to find its move.

**findMove(self, move_history)**

Uses the Minimax algorithm to select the next move based on the
board's current state (move_history). Returns an integer numbered 0-6
representing the column that has been selected for the move.

### PlayerAB(Player)

**alphaBeta(self, board, depth, alpha, beta)**

Iterates through the Minimax algorithm using Alpha-Beta pruning
to select a move based on the input board and depth, using the 
input max_depth and heuristic parameters to determine how far ahead 
and by what heuristic the algorithm should look to find its move. 
Returns a tuple with the first element being the selected move
and the second argument being the determined value of that move.

**findMove(self, move_history)**

Uses the Alpha-Beta algorithm to select the next move based on the
board's current state (move_history). Returns an integer numbered 0-6
representing the column that has been selected for the move.

### PlayerMC(Player)

**monteCarlo(self, board)**

Implements the Monte Carlo algorithm to select the next move based on
the input "board".

**findMove(self, move_history)**

Uses the Monte Carlo algorithm to select the next move based on the
board's current state (move_history). Returns an integer numbered 0-6
representing the column that has been selected for the move.
