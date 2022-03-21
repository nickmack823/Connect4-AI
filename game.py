import sys

from player import *
import time
import pygame
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

COLUMN_COUNT = 7
ROW_COUNT = 6
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE/2 - 5)
width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE
screen_size = (width, height)

class Game:

    def __init__(self, player1, player2, move_history=[]):
        self.move_history = move_history
        self.player1 = player1
        self.player2 = player2
        self.total_moves_p1, self.total_moves_p2 = 0, 0
        self.time_elapsed_p1, self.time_elapsed_p2 = 0, 0
        self.total_time = 0
        self.results = {player1.label: 0, player2.label: 0, 'Draw': 0}
        self.board = Board()

    def playGame(self):
        board = self.board
        self.player1.moves_considered, self.player2.moves_considered = 0, 0
        print(self.player1.label + " vs. " + self.player2.label)

        while not board.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit
                elif event.type == pygame.MOUSEMOTION:
                    if board.turn == 1:
                        x = event.pos[0]
                        self.drawHoveringPiece(x, RED)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    move = None
                    if board.turn == 1:
                        print("Player 1 turn")
                        x = event.pos[0]
                        col = int(math.floor(x/SQUARE_SIZE))
                        print(col)

                        time_start = time.time()
                        move = self.player1.findMove(board.move_history, col)
                        # User attempts invalid move
                        if move == None:
                            continue
                        time_end = time.time()
                        self.time_elapsed_p1 += time_end - time_start
                        self.drawPiece(move, board.getMoveRow(move), RED)
                        print("Player 1 move: " + str(move))
                    if board.turn == 2:
                        print("Player 2 turn")
                        time_start = time.time()
                        move = self.player2.findMove(board.move_history)
                        time_end = time.time()
                        self.time_elapsed_p2 += time_end - time_start
                        self.drawPiece(move, board.getMoveRow(move), YELLOW)
                        print("Player 2 move: " + str(move))
                    print(move)
                    board.makeMove(move)
                    board.printBoard()

                    self.total_moves_p1 += self.player1.moves_considered
                    self.total_moves_p2 += self.player2.moves_considered

                    if board.winner == 1:
                        print("Player 1 wins.")
                    elif board.winner == 2:
                        print("Player 2 wins.")
                    elif board.winner == 0:
                        print("Draw.")
                    if board.winner is not None:
                        self.recordResult(board.winner)

    def recordResult(self, result):
        if result == 1:
            self.results[self.player1.label] += 1
        elif result == 2:
            self.results[self.player2.label] += 1
        else:
            self.results["Draw"] += 1
        self.total_moves_p1 += self.player1.moves_considered
        self.total_moves_p2 += self.player2.moves_considered

    def testSuite(self, n):
        randPlayer = PlayerRandom()
        minimaxPlayer = PlayerMM(3, 1) # Uses depth 3 and heuristic 1 by default
        alphaBetaPlayer = PlayerAB(3, 1) # Uses depth 3 and heuristic 1 by default
        monteCarloPlayer = PlayerMC(100) # Performs 100 test games by default
        players = [randPlayer, minimaxPlayer, alphaBetaPlayer, monteCarloPlayer]
        games = []
        matchups = []

        # Generate a Game for all possible matchups given the Player instances we have
        for player in players:
            # Random doesn't deserve to be player 1
            if player.label == "Random":
                continue
            for otherPlayer in players:
                # Avoid putting Player against itself
                if otherPlayer != player:
                    matchup = player.label + "/" + otherPlayer.label
                    reversedMatchup = otherPlayer.label + "/" + player.label
                    # Create Game for matchup if these two Players aren't already set to go against each other
                    if matchup not in matchups and reversedMatchup not in matchups:
                        matchups.append(matchup)
                        game = Game(player, otherPlayer)
                        games.append(game)

        # Play each game in games n times
        for iteration in range(0, n):
            for game in games:
                game.playGame()
        self.printResults(games, n)

    def printResults(self, games, n):
        for game in games:
            p1 = game.player1.label
            p2 = game.player2.label
            if len(games) == 1:
                game_number = " "
            else:
                game_number = " " + str(games.index(game) + 1) + " "
            print("\nGAME" + game_number + "RESULTS (" + p1 + " vs. " + p2 + ")\n")
            print(p1 + " vs. " + p2 + " (" + str(n) + " games)")
            if p1 == "Minimax" or p1 == "Alpha-Beta":
                print(p1 + " depth: " + str(game.player1.max_depth))
            if p2 == "Minimax" or p2 == "Alpha-Beta":
                print(p2 + " depth: " + str(game.player2.max_depth))
            if p1 == "Monte Carlo":
                print("Random games played per possible move (Monte Carlo): " + str(game.player1.test_total))
            elif p2 == "Monte Carlo":
                print("Random games played per possible move (Monte Carlo): " + str(game.player2.test_total))
            print("Results: " + str(game.results))
            print("\nPlayer 1 (" + p1 + ")")
            print("Total moves considered: " + "{:,}".format(game.total_moves_p1))
            print("Average moves considered per game: " + "{:,}".format(game.total_moves_p1 / n))
            print("Time spent considering moves: " + str(round(game.time_elapsed_p1, 2)) + " seconds")
            print("Average time spent per game: " + str(round(game.time_elapsed_p1 / n, 2)) + " seconds")
            print("\nPlayer 2 (" + p2 + ")")
            print("Total moves considered: " + "{:,}".format(game.total_moves_p2))
            print("Average moves considered per game: " + "{:,}".format(game.total_moves_p2 / n))
            print("Time spent considering moves: " + str(round(game.time_elapsed_p2, 2)) + " seconds")
            print("Average time spent per game: " + str(round(game.time_elapsed_p2 / n, 2)) + " seconds")

    @classmethod
    def getPlayer(cls, selection):
        if selection == 1:
            return "Minimax"
        elif selection == 2:
            return "Alpha-Beta"
        elif selection == 3:
            return "Monte Carlo"
        elif selection == 4:
            return "Manual"
        else:
            return None

    @classmethod
    def getOpponent(cls, selection):
        opponents = ["Random", "Minimax", "Alpha-Beta", "Monte Carlo"]
        for opponent in opponents:
            if opponents.index(opponent) == selection-1:
                return opponent
        # Returns None if invalid input
        return None

    def drawBoard(self):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE + SQUARE_SIZE/2),
                                                   int(r*SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

    def drawPiece(self, column, row, color):
        pygame.draw.circle(screen, color, (int(column * SQUARE_SIZE + SQUARE_SIZE / 2),
                                           int(row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE - SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

    def drawHoveringPiece(self, x, color):
        pygame.draw.rect(screen, BLACK, (0,0,width,SQUARE_SIZE))
        pygame.draw.circle(screen, color, (x, int(SQUARE_SIZE/2)),RADIUS)
        pygame.display.update()

# if __name__ == "__main__":
#     print("Welcome to Connect Four!")
#     print("Would you like to run the standard test suite (1), or would you like to customize your game (2)?")
#     game_suite = int(input())
#     if game_suite == 1:
#         print("Games to run in the test suite: ")
#         n = int(input())
#         g1 = Game(PlayerRandom(None), PlayerRandom(None))
#         total_time = time.time()
#         g1.testSuite(n)
#         total_time = time.time() - total_time
#         print("\nTOTAL TIME ELAPSED: " + str(round(total_time, 2)) + " seconds.")
#     else:
#         print("Please select your player type: (1) Minimax, (2) Alpha-Beta, (3) Monte Carlo, (4) Manual")
#         character = int(input())
#         # Get player type from input
#         player_type = Game.getPlayer(character)
#         if player_type is None:
#             print("You did not enter a valid option")
#         else:
#             if player_type == "Minimax" or player_type == "Alpha-Beta":
#                 depth = int(input("What do you want the maximum depth of your search to be: "))
#                 heuristic = int(input("Which heuristic do you want to use (1, 2, or 3): "))
#                 if player_type == "Minimax":
#                     player = PlayerMM(depth, heuristic)
#                 elif player_type == "Alpha-Beta":
#                     player = PlayerAB(depth, heuristic)
#             elif player_type == "Monte Carlo":
#                 tests = int(input("Monte Carlo test count per move: "))
#                 player = PlayerMC(tests)
#             else:
#                 player = ManualPlayer()
#             print("Please select your opponent: (1) Random, (2) Minimax, (3) Alpha-Beta, (4) Monte Carlo")
#             opponent = int(input())
#             opponent_type = Game.getOpponent(opponent)
#             if opponent_type is None:
#                 print("You did not enter a valid option")
#             else:
#                 if opponent_type == "Minimax" or opponent_type == "Alpha-Beta":
#                     opponent_depth = int(input("Opponent maximum depth: "))
#                     opponent_heuristic = int(input("Opponent heuristic (1, 2, or 3): "))
#                     if opponent_type == "Minimax":
#                         opponent = PlayerMM(opponent_depth, opponent_heuristic)
#                     elif opponent_type == "Alpha-Beta":
#                         opponent = PlayerAB(opponent_depth, opponent_heuristic)
#                 elif opponent_type == "Monte Carlo":
#                     opponent_tests = int(input("Opponent Monte Carlo test count per move: "))
#                     opponent = PlayerMC(opponent_tests)
#                 else:
#                     opponent = PlayerRandom()
#
#                 game_count = int(input("How many games would you like to play: "))
#                 g = Game(player, opponent)
#                 for game in range(0, game_count):
#                     g.playGame()
#                 g.printResults([g], game_count)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    p1 = ManualPlayer()
    p2 = PlayerRandom()
    g = Game(p1, p2)
    g.drawBoard()

    g.playGame()